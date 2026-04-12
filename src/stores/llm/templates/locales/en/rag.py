from string import Template

### RAG PROMPT ###

### System ###

system_prompt =Template("\n".join([
    "You are an assistant to generate a response for the user.",
    "You will be provided by a set of document associated with the user's query.",
    "You have to generate response based on the documents provided.",
    "Ignore the documents tha are not relavant to the user's query.",
    "You can applogize to the user if you are not able to generate a response.",
    "You have to generate reponse in the same language as the user's query.",
    "Be polite and respectful to the user.",
    "Be precise and conies in your response. Avoid unnecessary information.",

]))


### Document ###
document_prompt = Template(
    "\n".join([
    "## Document No: $doc_num",
    "### Content: $chunk_text",

    ])
)


### Footer ###
footer_template = Template("\n".join([
    "Based only on the above document, please generate an answer for the user.",
    "## Question: $query",
    "",
    "## Answer:",
]))