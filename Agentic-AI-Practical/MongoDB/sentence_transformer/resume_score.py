import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import PyPDF2


def extract_text_from_pdf(pdf_path):
    """
    Extracts text from a PDF File.
    """

    text = ""

    with open(pdf_path,"rb") as file:
        reader = PyPDF2.PdfReader(file)

        for page in reader.pages :
            text += page.extract_text()
        
    return text

def similarity(job_desc,resume_text):
    """
    Computes semantic similarity between JD and resume text.
    """

    model = SentenceTransformer('all-MiniLM-L6-v2')

    #encode both jd and job description
    embeddings = model.encode([job_desc,resume_text])

    jd_embedding = embeddings[0].reshape(1,-1)
    resume_embedding = embeddings[1].reshape(1,-1)

    # build Faiss index for similarity search
    dimension = jd_embedding.shape[1]
    index = faiss.IndexFlatIP(dimension)
    index.add(jd_embedding)

    Similarity,_=index.search(resume_embedding,k=1)
    score = float(Similarity[0][0])

    #convert cosine similarity to percentage

    percentage = round(score*100,2)
    return percentage


def main():
    print("===========Resume shortlisting console Application=================")

    # take job description input

    jd = input("\n Enter the job description:\n")

    #take pdf path as input

    pdf_path = input("Enter the pdf path : ")

    resume_text = extract_text_from_pdf(pdf_path)

    # compute similarity percentage

    similarity_percentage = similarity(jd,resume_text)

    print(f"\n Resume Matching Score : {similarity_percentage}%")

    if similarity_percentage>=70:
        print(f"Your resume are shortlisted")
    else:
        print(f"Apolgies your resume was not shortlisted.")


if __name__=="__main__":
    main()