import openai
import json
import os


def ai_answers(organization,
               api_key,
               prompt="\n\n###",
               model="text-davinci-003",              
               temperature=0.7,
               max_tokens=400,
               top_p=1,
               best_of =1,
               frequency_penalty=0,
               presence_penalty=0,
               kep_first=True):
    try:
      openai.organization = organization
      openai.api_key = api_key
      response = openai.Completion.create(
                                          model=model,
                                          prompt=prompt,
                                          temperature=temperature,
                                          max_tokens=max_tokens,
                                          top_p=top_p,
                                          best_of =1,
                                          frequency_penalty=0,
                                          presence_penalty=0
                                        )
      json_data = json.loads(str(response))
      usage = json_data["usage"]
      if kep_first:
        text = json_data['choices'][0]['text']
      else:
        if len(json_data['choices'])>1:
          text = ''
          for s in d["choices"]:
              i=+1
              text = text+f'var {i}\n'+s['text']+'\n'
      return {'text':text,'usage':usage}
    except:
      return None