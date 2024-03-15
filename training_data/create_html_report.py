import json


def generate_html_report(jsonl_file, output_file):
    with open(jsonl_file, 'r') as file:
        data = [json.loads(line) for line in file]

    html = '''
<html>
<head>
<title>HTML Report</title>
<!-- Include Bootstrap CSS -->
<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css">
<style>
    /* Prevent table from overflowing and enable scrolling within cells if needed */
    .table-wrapper {
        max-width: 100%;
    }
    .solution-cell {
        max-height: 20em; /* Adjust based on the desired number of lines and line height */
        overflow-y: auto; /* Enable vertical scrolling within the cell */
        word-wrap: break-word;
        width: 100%;
    }
    /* Ensure table columns take up half the width */
    .table th, .table td {
        width: 50%;
        vertical-align: top;
    }
</style>
</head>
<body>
<div class="container">
    <div class="table-wrapper">
        <table class="table table-bordered">
            <thead class="thead-light">
                <tr>
                    <th scope="col">Problem</th>
                    <th scope="col">Solution</th>
                </tr>
            </thead>
            <tbody>
    '''
    for item in data:
        problem = item.get('problem', '').replace(
            '\n', '<br>')  # Convert line breaks for HTML
        solution = item.get('solution', '').replace(
            '\n', '<br>')  # Convert line breaks for HTML
        solution_display = '<code class="solution-cell">' + solution + '</code>'
        html += f'<tr>\n<td>{problem}</td>\n<td>{solution_display}</td>\n</tr>\n'

    html += '''
            </tbody>
        </table>
    </div>
</div> <!-- End of container -->
</body>
</html>
    '''

    with open(output_file, 'w') as file:
        file.write(html)

generate_html_report(
    'train.jsonl', 'train.html')
