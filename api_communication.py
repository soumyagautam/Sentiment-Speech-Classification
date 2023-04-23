import json
import requests
import time

upload_endpoint = 'https://api.assemblyai.com/v2/upload'
transcript_endpoint = "https://api.assemblyai.com/v2/transcript"
headers = {
    'authorization': "YOUR ASSEMBLY AI API KEY"
}


# Uploading the audio file to the Assembly AI Server
def upload(filename):
    def read_file(start_filename, chunk_size=5242880):
        with open(start_filename, 'rb') as _file:
            while True:
                data = _file.read(chunk_size)
                if not data:
                    break
                yield data

    upload_response = requests.post(upload_endpoint,
                                    headers=headers,
                                    data=read_file(filename)
                                    )

    audio_url = upload_response.json()["upload_url"]
    return audio_url


# Posting the request for transcription
def transcribe(audio_url, sentiment_analysis):
    transcript_request = {
        "audio_url": audio_url,
        "sentiment_analysis": sentiment_analysis
    }
    transcript_response = requests.post(transcript_endpoint, json=transcript_request, headers=headers)
    job_id = transcript_response.json()["id"]
    return job_id


# Checking whether the transcription is ready or not
def poll(transcript_id):
    polling_endpoint = transcript_endpoint + "/" + transcript_id
    polling_response = requests.get(polling_endpoint, headers=headers)
    return polling_response.json()


# Returns the polling response after polling is completed and check whether there was an error in this process
def get_transcription_result_url(audio_url, sentiment_analysis):
    transcript_id = transcribe(audio_url, sentiment_analysis)
    while True:
        data = poll(transcript_id)
        if data["status"] == "completed":
            return data, None
        elif data["status"] == "error":
            return data, data["error"]
        print("Waiting 30 seconds...")
        time.sleep(30)


# Saving transcription and sentiment analysis or error
def save_transcript(audio_url, title, sentiment_analysis=False):
    data, error = get_transcription_result_url(audio_url, sentiment_analysis)

    if data:
        text_filename = title + ".txt"
        with open(text_filename, "w") as f:
            f.write(data["text"])
        if sentiment_analysis:
            filename = title + "_sentiments.json"
            with open(filename, "w") as f:
                sentiments = data["sentiment_analysis_results"]
                json.dump(sentiments, f, indent=4)
        print("Transcription Saved!!")
    elif error:
        print("Error!!", error)
