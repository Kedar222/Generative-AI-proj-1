from dotenv import load_dotenv
import streamlit as st
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from pydantic import BaseModel, Field
from typing import List, Optional
from langchain_core.output_parsers import PydanticOutputParser

load_dotenv()

# ---------- Page setup ----------
st.set_page_config(
    page_title="CineSage | Movie Insights",
    page_icon="🎬",
    layout="centered",
)

st.title("🎬 CineSage")
st.subheader("Movie Insights Extractor")
st.write("Paste a movie paragraph to extract structured information.")

# ---------- LLM ----------
@st.cache_resource
def load_model():
    return ChatGroq(
        model="openai/gpt-oss-120b",
        temperature=0.3,
    )

model = load_model()


# ---------- Output schema ----------
class Movie(BaseModel):
    title: str = Field(description="Movie title")
    release_year: Optional[int] = Field(default=None, description="Release year")
    genre: List[str] = Field(default_factory=list)
    director: Optional[str] = None
    cast: List[str] = Field(default_factory=list)
    rating: Optional[float] = None
    summary: str


parser = PydanticOutputParser(pydantic_object=Movie)

prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """Extract movie information only from the paragraph provided.
Do not invent details. If information is missing, use null for optional fields
and an empty list for list fields. Write a concise summary.
{format_instructions}""",
    ),
    ("human", "{paragraph}"),
])


# ---------- Streamlit UI ----------
paragraph = st.text_area(
    "Movie paragraph",
    placeholder="Example: Interstellar is a 2014 science-fiction film directed by Christopher Nolan...",
    height=220,
)

if st.button("✨ Extract Movie Information", type="primary", use_container_width=True):
    if not paragraph.strip():
        st.warning("Please enter a movie paragraph first.")
    else:
        try:
            with st.spinner("Analyzing the movie paragraph..."):
                final_prompt = prompt.invoke({
                    "paragraph": paragraph,
                    "format_instructions": parser.get_format_instructions(),
                })
                response = model.invoke(final_prompt)
                movie = parser.invoke(response)

            st.success("Movie information extracted!")

            st.markdown("### 🎥 Movie Details")
            col1, col2 = st.columns(2)

            with col1:
                st.markdown("**Title**")
                st.write(movie.title)

                st.markdown("**Release Year**")
                st.write(movie.release_year if movie.release_year is not None else "Not mentioned")

                st.markdown("**Director**")
                st.write(movie.director or "Not mentioned")

                st.markdown("**Rating**")
                st.write(movie.rating if movie.rating is not None else "Not mentioned")

            with col2:
                st.markdown("**Genre**")
                st.write(", ".join(movie.genre) if movie.genre else "Not mentioned")

                st.markdown("**Cast**")
                st.write(", ".join(movie.cast) if movie.cast else "Not mentioned")

            st.markdown("### 📝 Summary")
            st.write(movie.summary)

            with st.expander("View structured data"):
                st.json(movie.model_dump())

        except Exception as e:
            st.error("Could not extract the movie information. Check your API key, connection, and model response.")
            st.caption(f"Technical details: {e}")
