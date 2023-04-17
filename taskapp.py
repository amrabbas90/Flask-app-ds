from flask import Flask, jsonify, request

CRapp = Flask(__name__)

TOKEN = 'hiring'

# Define a list of tasks
tasks = [
    {
        'id': 1,
        'question': 'We have fair coin. What is the probability that all first 5 tosses are heads?',
        'correct_answer': 0.03125
    },
    {
        'id': 2,
        'question': 'We have fair coin. We tossed it 5 times and got following sequence: HTTHH. What is the probability that 6th toss will be H?',
        'correct_answer': 0.5
    },
    {
        'id': 3,
        'question': 'Two cards are drawn from a deck of 52 cards. Find the probability that they are both kings if the first card is REPLACED. Round to the third decimal place.',
        'correct_answer': 0.006
    },
    {
        'id': 4,
        'question': 'Two cards are drawn from a deck of 52 cards. Find the probability that they are both kings if the first card is NOT REPLACED. Round to the third decimal place.',
        'correct_answer': 0.005
    },
    {
        'id': 5,
        'question': 'We have dice. We roll it 100 times. What is the probability that out from 100 rollings a six will show up exactly 15 times? Round to the first decimal place.',
        'correct_answer': 0.1
    },
    {
        'id': 6,
        'question': 'For Careem there are 3 car providers: A, B, C. Provider A has 2000 cars, provider B has 3000 cars, provider C has 5000 cars. On average we know that 95% of cars A are not broken, for B 80% of cars are not broken, for C 90% of cars are not broken. One random car was chosen and it appeared that it was broken. Find the probability that the manufacturer was B.',
        'correct_answer': 0.5
    },
]

# Define a list to store submitted answers
answers = []

@CRapp.route('/describe', methods=['POST'])
def describe():
    # Check if the user is authorized to access the endpoint
    if request.headers.get('token') != TOKEN:
        return jsonify({'message': 'Unauthorized access.'}), 401
    
    # Return a message to the user with instructions for the next step
    return jsonify({'message': 'Well done! Now for the same API use method /get_task, call it with GET request with empty payload and empty headers.'})

@CRapp.route('/get_task', methods=['GET'])
def get_task():
    # Check if the user is authorized to access the endpoint
    if request.headers.get('token') != TOKEN:
        return jsonify({'message': 'Unauthorized access.'}), 401
    
    # Construct a dictionary with the task questions
    task_dict = {
        f"task_{task['id']}": task['question']
        for task in tasks
    }
    task_dict["message"] = "You have now 6 tasks. Send the answers to method with POST method to /send_answers with JSON in body, example of JSON can be found by following link: https://pastebin.com/TBGs4pRm"
    
    # Return the task questions to the user
    return jsonify(task_dict)

@CRapp.route('/send_answers', methods=['POST'])
def send_answers():
    # Check if the user is authorized to access the endpoint
    if request.headers.get('token') != TOKEN:
        return jsonify({'message': 'Unauthorized access.'}), 401
    
    # Get the submitted answers from the request body
    submitted_answers = request.json
    
    # Check that all tasks are present in the submitted answers
    if not all(f"task_{task['id']}" in submitted_answers for task in tasks):
        return jsonify({'message': 'Missing answers.'}), 400
    
    # Check that all answers are valid numbers
    for task_id, answer in submitted_answers.items():
        if not isinstance(answer, (float, int)):
            return jsonify({'message': f'Answer to {task_id} is not a valid number.'}), 400
    
    # Calculate the number of correct answers
    num_correct = 0
    for task in tasks:
        task_id = f"task_{task['id']}"
        if submitted_answers[task_id] == task['correct_answer']:
            num_correct += 1
    
    # Calculate the total score and append the answers to the list
    score = round(num_correct / len(tasks), 2)
    answers.append(submitted_answers)
    
    # Return a message to the user based on the score
    if score == 1:
        message = 'Well done!'
    else:
        message = 'Please try again. Your answers are incorrect.'
    return jsonify({'message': message})
if __name__ == '__main__':
    CRapp.run(debug=True,host='0.0.0.0')