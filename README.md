# 📚 Adaptive Study Tutor

An AI-powered personalized learning assistant that explains syllabus concepts, generates quizzes, evaluates student performance, remembers weak topics, and creates personalized revision plans.

The system combines **LangGraph, LangChain, RAG, ChromaDB, MCP, Tavily, SQLite, and Streamlit** to provide an adaptive learning experience.

---

## 1. Introduction

Students learn at different speeds and have different levels of understanding. However, traditional classrooms generally follow the same teaching pace for everyone.

As a result, students may struggle with specific concepts without receiving enough individual practice or feedback.

The **Adaptive Study Tutor** is designed to address this problem by providing a personalized AI-based learning environment.

The tutor can:

- Explain syllabus concepts using educational knowledge sources.
- Provide source references for explanations.
- Generate quizzes based on a selected topic and difficulty.
- Evaluate student answers.
- Store quiz performance in SQLite.
- Identify weak topics from previous attempts.
- Explain weak concepts again when performance is low.
- Generate a new adaptive quiz.
- Create personalized revision plans based on weak topics and available study time.
- Use web search through Tavily when the local knowledge base is insufficient.
- Protect quiz answers until the student submits their responses.

The system is orchestrated using **LangGraph**, allowing different specialized agents to work together through shared state and conditional routing.

---

## 2. Problem Statement

Traditional learning environments face several challenges:

- Students learn at different speeds.
- Classroom teaching generally follows a common pace.
- Students may not receive enough practice on weak concepts.
- Teachers cannot continuously track every student's performance.
- Revision plans are often not personalized to individual weaknesses.

The Adaptive Study Tutor addresses these challenges by continuously using student performance to personalize future learning activities.

---

## 3. Objectives

The main objectives are:

1. Explain educational concepts using syllabus and textbook content.
2. Provide reliable source references for explanations.
3. Generate topic-specific quizzes.
4. Evaluate student answers and provide feedback.
5. Store student performance history.
6. Identify weak topics.
7. Adapt learning based on quiz performance.
8. Generate new quizzes after weak performance.
9. Prevent unlimited adaptive learning loops using an iteration limit.
10. Generate personalized revision plans.
11. Use supplementary web information when the local knowledge base is insufficient.
12. Provide a simple interactive Streamlit interface.
13. Prevent the tutor from revealing quiz answers before submission.

---

## 4. Target Users

The system can be used by:

- School students
- College students
- Self-learners
- Teachers who want to support student practice

---

## 5. Knowledge Base

The Adaptive Study Tutor uses a **Retrieval-Augmented Generation (RAG)** pipeline to retrieve relevant educational content from locally provided:

- Textbook chapters
- Syllabus PDFs
- University course materials
- Educational notes

### Copyright Notice

**Copyrighted textbook PDFs are not included in this GitHub repository.**

The project is designed so that users can provide their own educational materials that they are authorized to use.

Place authorized PDF files locally inside:

```text
knowledge_base/
└── physics/
    ├── your_textbook.pdf
    └── your_course_material.pdf