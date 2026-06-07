# SmartEval
SmartEval – AI-Powered Smart Exam Evaluation Platform using Machine Learning and NLP

### Abstract

SmartEval is a research-based B.Tech final year project that aims to automate the evaluation of descriptive answers using Artificial Intelligence, Machine Learning, and Natural Language Processing (NLP). Traditional manual evaluation is time-consuming and may introduce inconsistencies. This system provides an intelligent evaluation framework that analyzes student responses and generates scores automatically.

### Problem Statement

Manual assessment of subjective answers requires significant time and effort from educators. The objective of this research is to develop an AI-driven evaluation system capable of assessing student answers accurately and efficiently while reducing human workload.

### Research Objectives

- Automate descriptive answer evaluation
- Improve consistency in assessment
- Reduce evaluation time
- Utilize NLP techniques for semantic analysis
- Provide instant feedback and results

### Methodology

1. Student submits answers through the platform.
2. Answers are processed using NLP techniques.
3. Machine Learning models analyze the similarity and quality of responses.
4. Scores are generated automatically.
5. Results are stored and displayed to users.

### System Modules

#### Admin Panel
- Add, update, and delete teachers
- Add, update, and delete students
- Manage system users
- Monitor overall system activities

#### Teacher Panel
- Monitor examinations
- Review evaluation results
- Create, update, and delete examinations
- Track student performance

#### Student Panel
- Attend examinations
- Submit answers
- View results and scores

### Technologies Used

- Python
- Streamlit
- SQLite
- Machine Learning
- Natural Language Processing (NLP)
- Deep Learning

### Project Structure

- app.py – Main application
- admin_page.py – Admin operations
- teacher.py – Teacher module
- student.py – Student module
- model.py – AI/NLP evaluation engine
- database.py – Database management
- result_page.py – Result generation
- style.css – User interface styling

## Future Scope

- Improve model accuracy through additional training and dataset expansion.
- Experiment with advanced transformer models such as RoBERTa and DeBERTa.
- Enhance semantic understanding for descriptive answer evaluation.
- Support multilingual answer assessment.
- Implement plagiarism detection and detailed feedback generation.
- Deploy the system as a scalable cloud-based platform.

  ### Workflow

1. Student submits an answer.
2. Text preprocessing is performed.
3. BERT generates contextual embeddings.
4. BiLSTM extracts sequential features.
5. Pooling creates a fixed-length representation.
6. Cosine Similarity compares student and reference answers.
7. The system generates the final score automatically.

## Proposed Architecture

Student Answer
      ->
Text Preprocessing
      ->
BERT Embedding Layer
      ->
BiLSTM Layer
      ->
Pooling Layer
      ->
Cosine Similarity
      ->
Score Prediction
      ->
Result Generation

### Note

This project is a research prototype developed for academic purposes. Evaluation accuracy depends on the quality of training data and model parameters and is subject to further improvement.

## Project Team

### Team Members

- Aniket Saha
- Diya Majumder
- Julphikar Haque
- Baishali Saha

**B.Tech in Computer Science and Engineering**  
**Siliguri Institute of Technology**

### Project Mentor

**Ms. Sampa Das**  
Department of Computer Science and Engineering  
Siliguri Institute of Technology
