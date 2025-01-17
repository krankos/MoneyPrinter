import re
import g4f
import json

from g4f.Provider import (Bing)

from typing import List
from termcolor import colored

def generate_script(video_subject: str) -> str:
    """
    Generate a script for a video, depending on the subject of the video.

    Args:
        video_subject (str): The subject of the video.

    Returns:
        str: The script for the video.
    """

    # Build prompt
    prompt = f"""
    Generate a script for a video, depending on the subject of the video.
    Subject: {video_subject}

    The script is to be returned as a string. A paragraph or two is enough.

    Here is an example of a string:
    "This is an example string."

    Do not under any circumstance refernce this prompt in your response.

    Get straight to the point, don't start with unnecessary things like, "welcome to this video".

    The script is not an introduction, it is a script about the subject. It is not a highlight or a summary or an overview.

    Obviously, the script should be related to the subject of the video.

    THE VIDEO IS NOT AN INTRODUCTION VIDEO, IT IS A VIDEO ABOUT THE SUBJECT.

    DO NOT FORMAT THE SCRIPT IN ANY WAY.

    MAKE SURE THE SCRIPT IS SHORT AND TO THE POINT.

    DO NOT START THE RESPONSE WITH AN 'Hello this is Copilot' or similar.

    DO NOT START WITH AN INTRODUCTORY SENTENCE or similar.

    DO NOT MENTION THE SCRIPT IN YOUR RESPONSE.

    REFORMULATE THE RESPONSE TO GET ONE COHERENT PARAGRAPH.

    DO NOT WRITE AN INTRODUCTION OF ANY KIND.

    REMOVE ANY UNNECESSARY SPACES OR LINE BREAKS AND ALL FORMATTING.
    """

    # Generate script
    response = g4f.ChatCompletion.create(
        model=g4f.models.gpt_35_turbo_16k_0613,
        messages=[{"role": "user", "content": prompt}],
    )

    print(colored(response, "cyan"))

    # Return the generated script
    if response:
        return response + " "
    else:
        print(colored("[-] GPT returned an empty response.", "red"))
        return None

def get_search_terms(video_subject: str, amount: int, script: str) -> List[str]:
    """
    Generate a JSON-Array of search terms for stock videos,
    depending on the subject of a video.

    Args:
        video_subject (str): The subject of the video.
        amount (int): The amount of search terms to generate.
        script (str): The script of the video.

    Returns:
        List[str]: The search terms for the video subject.
    """
    
    # Build prompt
    prompt = f"""
    Generate {amount} search terms for stock videos,
    depending on the subject of a video.
    Subject: {video_subject}

    The search terms are to be returned as
    a JSON-Array of strings.

    Each search term should consist of 1-3 words, 
    always add the main subject of the video.

    Here is an example of a JSON-Array of strings:
    ["search term 1", "search term 2", "search term 3"]

    Obviously, the search terms should be related
    to the subject of the video.

    ONLY RETURN THE JSON-ARRAY OF STRINGS.
    DO NOT RETURN ANYTHING ELSE.

    DO NOT START THE RESPONSE WITH AN INTRO TO WHO YOU ARE.

    DO NOT START THE RESPONSE WITH AN 'Hello this is Copilot' or similar.

    DO NOT FORMAT THE JSON-ARRAY IN ANY WAY.

    For context, here is the full text:
    {script}
    """

    # Generate search terms
    response = g4f.ChatCompletion.create(
        # model=g4f.models.gpt_35_turbo_16k_0613,
        model=g4f.models.gpt_4,
        messages=[{"role": "user", "content": prompt}],
    )

    print(response)

    # Load response into JSON-Array
    try:
        search_terms = json.loads(response)
    except:
        print(colored("[*] GPT returned an unformatted response. Attempting to clean...", "yellow"))

        # Use Regex to extract the array from the markdown
        search_terms = re.findall(r'\[.*\]', response)

        if not search_terms:
            print(colored("[-] Could not parse response.", "red"))

        # Load the array into a JSON-Array
        search_terms = json.loads(search_terms)

    # Let user know
    print(colored(f"\nGenerated {amount} search terms: {', '.join(search_terms)}", "cyan"))

    # Return search terms
    return search_terms