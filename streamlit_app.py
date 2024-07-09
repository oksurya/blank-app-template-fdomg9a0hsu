import streamlit as st
import requests
from urllib.parse import urlparse, parse_qs

def extract_domain(url):
    parsed_url = urlparse(url)
    return parsed_url.netloc

def check_url(url):
    try:
        session = requests.Session()
        response = session.get(url, allow_redirects=True)
        final_url = response.url

        parsed_url = urlparse(final_url)
        query_params = parse_qs(parsed_url.query)

        cookies = session.cookies.get_dict()

        response_data = {
            "final_url": final_url,
            "Postrequest1": f"/send-request?request=setVisitor&status=1&vid={query_params.get('vid', [''])[0]}&imps=4&domain={extract_domain(final_url)}",
            "Postrequest2": f"/send-request?request=setVisitor&status=2&vid={query_params.get('vid', [''])[0]}&imps=5&domain={extract_domain(final_url)}",
            "Postrequest3": f"/send-request?request=setVisitor&status=3&vid={query_params.get('vid', [''])[0]}&imps=6&domain={extract_domain(final_url)}",
            "host": extract_domain(final_url),
            "cookies": cookies,
            "parameters": query_params,
            "directurl": f"https://gplinks.co/{query_params.get('lid', [''])[0]}/?pid={query_params.get('pid', [''])[0]}&vid={query_params.get('vid', [''])[0]}"
        }

        return response_data

    except Exception as e:
        return {"error": str(e)}

def send_request(request_param, status_param, imps_param, vid_param):
    try:
        data = {
            "request": request_param,
            "status": status_param,
            "imps": imps_param,
            "vid": vid_param,
        }

        response = requests.post("https://gplinks.com/track/data.php", data=data)

        response_data = {
            "status_code": response.status_code,
            "response_text": response.text,
        }

        return response_data

    except Exception as e:
        return {"error": str(e)}

# Streamlit UI
st.title('URL Checker and Request Sender')

url = st.text_input('Enter a URL to check:')
if st.button('Check URL'):
    if url:
        st.write("Checking URL...")
        result = check_url(url)
        st.json(result)
    else:
        st.error("Please enter a URL.")

st.sidebar.title('Send Request')
request_param = st.sidebar.selectbox('Request', ['setVisitor'])
status_param = st.sidebar.selectbox('Status', ['1', '2', '3'])
imps_param = st.sidebar.number_input('Impressions', min_value=0)
vid_param = st.sidebar.text_input('Visitor ID')

if st.sidebar.button('Send Request'):
    if request_param and status_param and imps_param and vid_param:
        st.write("Sending request...")
        result = send_request(request_param, status_param, imps_param, vid_param)
        st.json(result)
    else:
        st.sidebar.error("Please fill in all parameters.")

