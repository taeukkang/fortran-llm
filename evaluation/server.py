from flask import Flask, render_template
import json
import markdown

app = Flask(__name__, template_folder='templates')


with open('data/finetuned_code.json') as file:
    finetuned_codes = json.load(file)
    finetuned_ids = sorted(list(finetuned_codes.keys()),
                           key=lambda id: int(id))

with open('data/finetuned_eval.json') as file:
    finetuned_evals = json.load(file)

with open('data/baseline_code.json') as file:
    baseline_codes = json.load(file)

with open('data/baseline_eval.json') as file:
    baseline_evals = json.load(file)

with open('data/leetcode_problems.jsonl', 'r') as file:
    leetcode_data = {}
    for line in file:
        data = json.loads(line)
        leetcode_data[str(data['id'])] = data


@app.template_filter('markdown')
def markdown_filter(s):
    s = s.strip()
    return markdown.markdown(s, extensions=['fenced_code'])


@app.route('/')
def index():
    return render_template("index.html.jinja", finetuned_codes=finetuned_codes, leetcode_data=leetcode_data,
                           finetuned_evals=finetuned_evals, baseline_evals=baseline_evals)


@app.route('/<problem_id>/')
def result(problem_id):
    if problem_id not in finetuned_ids:
        return "ID not found", 404

    current_index = finetuned_ids.index(problem_id)

    prev_id = finetuned_ids[current_index -
                            1] if current_index > 0 else finetuned_ids[-1]
    next_id = finetuned_ids[current_index +
                            1] if current_index < len(finetuned_ids) - 1 else finetuned_ids[0]

    finetuned_code = finetuned_codes.get(problem_id, "Snippet not found")
    finetuned_eval = finetuned_evals.get(problem_id, "Snippet not found")
    baseline_code = baseline_codes.get(problem_id, "Snippet not found")
    baseline_eval = baseline_evals.get(problem_id, "Snippet not found")
    leetcode_problem = leetcode_data.get(
        problem_id, {"title": "Problem not found", "content": "Problem not found",
                     "c++": "Problem not found", "python": "Problem not found"})

    return render_template("result.html.jinja", snippet_id=problem_id, finetuned_code=finetuned_code,
                           finetuned_eval=finetuned_eval, baseline_eval=baseline_eval,
                           basemodel_code=baseline_code, leetcode_problem=leetcode_problem,
                           prev_id=prev_id, next_id=next_id)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5500)
