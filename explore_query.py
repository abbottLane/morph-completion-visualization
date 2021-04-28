from os import readlink
import subprocess
import csv

MODEL = "grammars/crk-infl-morpheme-completion.old.hfstol"


def main():
    queries = [
        "nâtam",
        "nôhtêyâpâkwêw",
        "tapahtiskwêyiyiwa",
        "takosiniyahko",
        "takosiniyani",
        "takosihki",
        "tahkoskêw",
        "tahkonamwak",
        "tahkahtam",
        "ta-wani-kiskisiw",
        "ta-tôtamiyit",
        "ta-tôtahkik",
        "ta-tâpwêw",
        "ta-nipahât",
        "ta-nipahâhkatosoyân",
        "ta-mîciyân",
        "ta-mîciyit",
        "ta-mîciw",
        "ta-mîcisocik",
        "ta-mâyi-kîsikâw",
        "ta-mânokêwak",
        "ta-kiskêyihtahk",
        "ta-itohtêt",
        "sêskisiw",
        "sêkisiwak",
        "sêkihik",
        "sâmahwêw",
        "sâkôcimiski",
        "sâkohihci",
        "sipwêhtatâwak",
        "saskahohtêw",
        "sakâyiw",
        "sakahpitêw",
        "pôyoyiwa",
        "pôsiw",
        "pôni-atoskêw",
        "pîkopayiyiwa"
    ]

    data = [["target_word", "prefix", "rank"]]
    for q in queries:
        for i,_ in enumerate(q):
            if i != 0:
                prefix = q[:i]
                result = invoke_fst_subprocess(prefix)
                rank_of_target = get_target_rank(query=q, query_result=result)
                data.append([q, prefix, rank_of_target])
    
    with open("data/tsv/cree-explore-words.tsv", "w") as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerows(data)

def get_target_rank(query, query_result):
    for i, completion in enumerate(query_result['completions']):
        if query.startswith(completion):
            return i+1

def invoke_fst_subprocess(pref):
    results = subprocess.run(
                    ["hfst-optimized-lookup", "-q", "-u", MODEL],
                    input=pref.encode('utf-8'),
                    stdout=subprocess.PIPE
                    )
    results = str(results.stdout.decode('utf-8')).split("\n")
    results = [x for x in results if " " not in x] # filter out the full-phrase completions
    return {"prefix": pref, "completions":results}


if __name__ == "__main__":
    main()