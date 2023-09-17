from django.shortcuts import render
from django.http import HttpResponse, StreamingHttpResponse
from langchain import LLMChain
import subprocess
import sys
from pathlib import Path

# Create your views here.


def index(request):
    request.session['seed'] = 0
    request.session['temperature'] = 0.7
    request.session['number_of_tokens'] = 169
    return render(request, template_name='index.html')


# def llmResponse(request):
#     userMessage = request.GET.get('userMessage')
#     print(userMessage)
#     llm_chain = LLMChain(prompt=prompt, llm=llm)
#     response = llm_chain.run(userMessage)
#     print(response)
#     return StreamingHttpResponse(response, content_type="text/plain")


def llmResponse(request):
    # stream stout

    if request.method == 'GET':
        prompt = request.GET.get('userMessage')

    elif request.method == 'POST':
        try:
            request.session['seed'] = int(request.POST.get('seed'))
            request.session['number_of_tokens'] = int(request.POST.get('maxNewTokens'))
            request.session['temperature'] = int(request.POST.get('temperature'))
        except (ValueError, TypeError):
            # Handle invalid input values here
            return HttpResponse("Invalid input values in the POST request.")
        return render(request, template_name='index.html')

    print(prompt)
    process = subprocess.Popen(
        [
            "mojo",
            "llama2.mojo",
            Path('stories110M.bin'),
            "-s",
            str(request.session['seed']),
            "-n",
            str(request.session['number_of_tokens']),
            "-t",
            str(request.session['temperature']/100),
            "-i",
            prompt,
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    text = ""
    for char in iter(lambda: process.stdout.read(1), b""):
        char_decoded = char.decode("utf-8", errors="ignore")
        text += char_decoded
    print(text)
    return StreamingHttpResponse(text, content_type="text/plain")

def parameter(request):
    return render(request, template_name='parameter.html')
