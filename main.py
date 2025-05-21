import os
import gradio as gr
from langchain_groq import ChatGroq
from langchain_core.runnables import Runnable
from chat_engine import conversation_prompt
from chat_engine import chapter_index
from chat_engine import tree_index_list
from chat_engine import select_index
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from pathlib import Path

groq_llm = ChatGroq(
    model_name="llama-3.3-70b-versatile",  
    temperature=0.2,  
    api_key=os.getenv('GROQ_API_KEY')
)

response_chain: Runnable = conversation_prompt | groq_llm

def gradio_chat(user_query, chat_history, index, tree_index_list=tree_index_list, chapter_index=chapter_index,response_chain=response_chain):
    
    if chat_history is None:
        chat_history=[]
    
    if user_query=="":
        chat_history.append(HumanMessage(user_query))
        chat_history.append(AIMessage("Kindly ask a question from the selected chapter."))
        return "Kindly ask a question from the selected chapter", chat_history
    
    vector_index=select_index(index)
    retriever1=vector_index.as_retriever(similarity_top_k=2)
    retrieved_nodes1=retriever1.retrieve(user_query)
    
    tree_index=tree_index_list[chapter_index[retrieved_nodes1[0].metadata["chapter"]]]
    if retrieved_nodes1[0].metadata["section"]=="poem":
        retriever = tree_index.as_retriever(similarity_top_k=4, retriever_mode="all_leaf")
        retrieved_nodes3=retriever.retrieve("summarize the poem")
        pext=""
        for content in retrieved_nodes3:
            pext=pext+' '+content.text.strip()
        context='Author: '+retrieved_nodes1[0].metadata['author']+'\nSection: '+retrieved_nodes1[0].metadata['section']+'\nChapter: '+retrieved_nodes1[0].metadata['chapter']+'\nContext: '+pext
        
    else:
        contextt=[]
        for text in retrieved_nodes1:
            contextt.append((text.metadata['page'], text.text))
        contextt.sort(key=lambda x:x[0])
        context1=[x[1] for x in contextt]
    
        retriever = tree_index.as_retriever(similarity_top_k=1,retriever_mode="root", 
                                            search_kwargs={"num_children":3})

        retrieved_nodes2=retriever.retrieve("summarize this chapter")
        
        for text in retrieved_nodes2:
            context1.append(text.text.strip())
        context="\n".join(context1)
        context='Author: '+retrieved_nodes1[0].metadata['author']+'\nSection: '+retrieved_nodes1[0].metadata['section']+'\nChapter: '+retrieved_nodes1[0].metadata['chapter']+'\nContext: '+context

    chat_history.append(HumanMessage(user_query))
    response=response_chain.invoke({"chat_history":chat_history[-12:], "user_query":user_query, "document_context":context})
    chat_history.append(AIMessage(response.content))
    
    return response.content, chat_history

def respond(message, chain_history, ui_history, index):

    ui_history.append({"role": "user", "content": message})
    response_text, updated_history = gradio_chat(message, chain_history, index=index)
    
    if ui_history is None:
        ui_history = []
    
    ui_history.append({"role": "assistant", "content": response_text})
    return "", updated_history, ui_history

def download_file(index):
    filepath=chapter_dir[index]
    return filepath

custom_css = """
#chatbot_interface {
    background: #f0f0f0;
    padding: 20px;
    border-radius: 10px;
}
/* Center the markdown text */
#welcome_markdown {
    text-align: center;
    margin: auto;
}
"""

with gr.Blocks(css=custom_css,fill_width=True) as demo:
    gr.Markdown("""
    # I’m Shalini ☺️ # 
    Your Creative Muse — Where Literature Dances, Art Breathes, and Philosophy Whispers 🎨📖🪞  
    Welcome to *Kaleidoscope* —  
    Where words don’t just sit still — they swirl, they shimmer, they *sing*.   
    Have a question from the 12th NCERT English textbook *Kaleidoscope*?  
    Ask — and I’ll reply with words that wander, wonder, and land like truth. 📚🌿 
    ---
    Let’s begin this soulful journey together:
    1. Pick your chapter from the dropdown below.  
    2. Step into the story with your question.  
    3. I’ll craft a reply — rhythmic, radiant, and rich with meaning. 🖼️💫
    """,elem_id="welcome_markdown")
    
    chapter_dir={"Broken Images":"Dataset/Drama/Broken_images.pdf", 
                 "Blood":"Dataset/Poems/Blood.pdf", 
                 "Flim Making":"Dataset/non_fiction/Flim_making.pdf", 
                 "Kubla Khan":"Dataset/Poems/Kubla_khan.pdf", 
                 "One Centimeter":"Dataset/Stories/One_centimetre.pdf",
              "I Sell My Dreams":"Dataset/Stories/I_sell_my_dreams.pdf", 
              "Poems By Blake":"Dataset/Poems/The_divine_image.pdf", 
              "Time and Time Again":"Dataset/Poems/Time_and_time_again.pdf", 
              "On Time":"Dataset/Poems/On_time.pdf",
              "Trees":"Dataset/Poems/Trees_emily_dickinson.pdf", 
              "On Science Fiction":"Dataset/non_fiction/On_science_fiction.pdf", 
              "The Argumentative Indian":"Dataset/non_fiction/The_argumentative_indian.pdf", 
              "Why The Novel Matters":"Dataset/non_fiction/Why_the_novel_matters.pdf",
              "Tomorrow":"Dataset/Stories/Tomorrow.pdf", 
              "A Lecture Upon The Shadow":"Dataset/Poems/A_lecture_upon_the_shadow.pdf", 
              "Freedom":"Dataset/non_fiction/Freedom_freedom.pdf", 
              "A Wedding in Brownsville":"Dataset/Stories/A_wedding_in_brownsville.pdf",
              "Eveline":"Dataset/Stories/eveline.pdf", 
              "Chandalika":"Dataset/Drama/Chandalika.pdf", 
              "The Wild Swans At Coole":"Dataset/Poems/The_wild_swans_at_coole.pdf", 
              "The Mark On The Wall":"Dataset/non_fiction/The_mark_on_the_wall.pdf"}
    
    chatbot = gr.Chatbot(label="Chat Interface", elem_id="chatbot_interface", type="messages")
    
    index=gr.State()
    with gr.Row():
        index=gr.Dropdown(
            choices=list(chapter_dir.keys()),
            label="Chapter",
            value="Broken Images",
            info="Select the chapter on which you would like to ask questions."
        )
        msg = gr.Textbox(label="Enter your query:", placeholder="Type your question here...", lines=2)
        
        d = gr.DownloadButton("Download Selected Chapter", visible=True)
        index.change(fn=download_file, inputs=index, outputs=d)
    
    chain_history = gr.State([])  # For LangChain message objects
    ui_history = gr.State([])       # For display, a list of dictionaries
    
    gr.Button("Glide In🎨").click(respond, [msg, chain_history, ui_history, index], [msg, chain_history, chatbot])

demo.launch(allowed_paths=["Dataset/Stories","Dataset/Drama",
                           "Dataset/Poems","Dataset/non_fiction"])
