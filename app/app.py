import streamlit as st
import requests

st.title('News sentiment analysis')

query = st.text_input('Enter a subject for news analysis')
if st.button('Submit'):
    if query:
        response = requests.post("http://127.0.0.1:8000/analyze-news", json={"query": query})
        if response.status_code == 200:
            data = response.json()
            if "error" in data:
                st.error(f"Error: {data['error']}")
            else:
                st.write(data.get('title', 'No Title Available'))
                audio_path = data.get('audio_path')

                if audio_path:
                    st.write('### Audio:')
                    st.audio(audio_path)
                else:
                    st.warning('No Audio Found')
                st.write("### News Summaries:")
                for title, summary in data['summaries'].items():
                    st.write(f"**{title}**")
                    st.write(summary)
                    st.write(f"Sentiment: {data['sentiments'].get(title, 'Unknown')}")
                    keywords = data['result'].get('unique_keywords', {}).get(title, [])
                    if keywords:
                        st.write(f"**Keywords:** {', '.join(keywords)}")
                    else:
                        st.write("**Keywords:** No keywords found.")
                    st.write("---")
                st.write("### Comparitive Analysis:")
                st.write(data["result"])

        else:
            st.error("Failed to fetch data. Please try again.")

