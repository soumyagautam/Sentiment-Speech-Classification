import json
from api_communication import save_transcript, upload


def save_video_sentiments(url):
    audio_url = upload(url)
    title = "output"
    save_transcript(audio_url, title, sentiment_analysis=True)


if __name__ == "__main__":
    save_video_sentiments("sample_recording.m4a")

    with open("output_sentiments.json", "r") as f:
        data = json.load(f)

    positives = []
    negatives = []
    neutrals = []

    for result in data:
        text = result["text"]
        if result["sentiment"] == "POSITIVE":
            positives.append(text)
        elif result["sentiment"] == "NEGATIVE":
            negatives.append(text)
        else:
            neutrals.append(text)

    n_pos = len(positives)
    n_neg = len(negatives)
    n_neu = len(neutrals)

    print("Number of Positives: ", n_pos)
    print("Number of Negatives: ", n_neg)
    print("Number of Neutrals: ", n_neu)

    ratio = n_pos / (n_pos + n_neg)
    print(f"Positive Ratio: {ratio:.3f}")
