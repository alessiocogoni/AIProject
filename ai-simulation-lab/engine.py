import os,json,urllib.request,urllib.error
SCENARIOS={'success':200,'empty':400,'invalid':422,'auth':401,'forbidden':403,'missing':404,'timeout':408,'rate_limit':429,'server':500,'unavailable':503,'offline':0,'malformed':502}
def simulate(name):
    status=SCENARIOS.get(name,400) if isinstance(name,str) else 400
    return dict(scenario=str(name),status=status,outcome='success' if status==200 else 'fallback' if status in (0,408,429,500,502,503) else 'rejected',handled=True)
def infer(prompt):
    if not isinstance(prompt,str) or not prompt.strip() or len(prompt)>4000:return simulate('invalid')
    token=os.getenv('HF_TOKEN')
    if not token:return dict(simulate('offline'),text='Modalità demo: nessuna inferenza reale.')
    try:
        payload=json.dumps(dict(model=os.getenv('HF_MODEL','Qwen/Qwen2.5-7B-Instruct'),messages=[dict(role='user',content=prompt)],max_tokens=256)).encode()
        req=urllib.request.Request('https://router.huggingface.co/v1/chat/completions',data=payload,headers={'Authorization':'Bearer '+token,'Content-Type':'application/json'})
        with urllib.request.urlopen(req,timeout=20) as response:
            answer=json.loads(response.read(1000000))['choices'][0]['message']['content']
            if not isinstance(answer,str):raise ValueError()
            return dict(simulate('success'),text=answer)
    except urllib.error.HTTPError as exc:return simulate(next((k for k,v in SCENARIOS.items() if v==exc.code),'server'))
    except (TimeoutError,OSError):return simulate('offline')
    except (ValueError,KeyError,IndexError,TypeError):return simulate('malformed')
