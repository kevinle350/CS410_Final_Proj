from dash import Dash, html, Input, Output, State, ctx
import dash_bootstrap_components as dbc
import requests

# Create Dash app
app = Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])

# Layout
app.layout = html.Div(
    style={
        "fontFamily": "Arial, sans-serif",
        "height": "100vh",
        "display": "flex",
        "backgroundColor": "#121212",  # Dark background
        "color": "#FFFFFF",            # Light text
    },
    children=[
        # Sidebar
        html.Div(
            style={
                "width": "500px",
                "backgroundColor": "#1E1E1E",  # Dark sidebar background
                "padding": "20px",
                "boxShadow": "2px 0 5px rgba(0, 0, 0, 0.5)",
            },
            children=[
                html.H2("Welcome to the Course Recommender!", style={"color": "#BBBBBB"}),
                html.P("We are here to help you.",
                    style={"color": "#888888", "lineHeight": "1.6"},
                ),
                html.P("Enter topics you are interested in learning about in the chat "
                    "and we will recommend a course for you to take!",
                    style={"color": "#888888", "lineHeight": "1.6"},
                ),
                html.Div(
                    children=[
                        dbc.Label("Select a Course:"),
                        dbc.Select(
                            id="course-dropdown",
                            options=[
                                {"label": "CS 598: Advanced Bayesian Modeling", "value": "Advanced Bayesian Modeling"},
                                {"label": "CS 525: Advanced Distributed Systems", "value": "Advanced Distributed Systems"},
                                {"label": "CS 441: Applied Machine Learning", "value": "Applied Machine Learning"},
                                {"label": "CS 498: Cloud Computing Applications", "value": "Cloud Computing Applications"},
                                {"label": "CS 598: Cloud Computing Capstone", "value": "Cloud Computing Capstone"},
                                {"label": "CS 435: Cloud Networking", "value": "Cloud Networking"},
                                {"label": "CS 445: Computational Photography", "value": "Computational Photography"},
                                {"label": "CS 463: Computer Security II", "value": "Computer Security II"},
                                {"label": "CS 598: Data Mining Capstone", "value": "Data Mining Capstone"},
                                {"label": "CS 416: Data Visualization", "value": "Data Visualization"},
                                {"label": "CS 411: Database Systems", "value": "Database Systems"},
                                {"label": "CS 598: Deep Learning for Healthcare", "value": "Deep Learning for Healthcare"},
                                {"label": "CS 425: Distributed Systems (Cloud Computing Concepts)", "value": "Distributed Systems"},
                                {"label": "CS 598: Foundations of Data Curation", "value": "Foundations of Data Curation"},
                                {"label": "CS 418: Interactive Computer Graphics", "value": "Interactive Computer Graphics"},
                                {"label": "CS 437: Internet of Things", "value": "Internet of Things"},
                                {"label": "CS 412: Introduction to Data Mining", "value": "Introduction to Data Mining"},
                                {"label": "STAT 420: Methods of Applied Statistics", "value": "Methods of Applied Statistics"},
                                {"label": "CS 447: Natural Language Processing", "value": "Natural Language Processing"},
                                {"label": "CS 450: Numerical Analysis", "value": "Numerical Analysis"},
                                {"label": "CS 484: Parallel Programming", "value": "Parallel Programming"},
                                {"label": "CS 598: Practical Statistical Learning", "value": "Practical Statistical Learning"},
                                {"label": "CS 421: Programming Languages and Compilers", "value": "Programming Languages and Compilers"},
                                {"label": "CS 519: Scientific Visualization", "value": "Scientific Visualization"},
                                {"label": "CS 427: Software Engineering I", "value": "Software Engineering I"},
                                {"label": "CS 410: Text Information Systems", "value": "Text Information Systems"},
                                {"label": "CS 513: Theory and Practice of Data Cleaning", "value": "Data Cleaning"},
                            ],
                            placeholder="Select a course",
                        ),
                    ],
                )
            ],
        ),
        # Chat Area
        html.Div(
            style={"flex": "1", "display": "flex", "flexDirection": "column"},
            children=[
                html.Div(
                    "Course Recommender",
                    style={
                        "backgroundColor": "#282C34",  # Darker header
                        "color": "#FFFFFF",
                        "padding": "10px",
                        "textAlign": "center",
                        "fontWeight": "bold",
                        "fontSize": "24px",
                    },
                ),
                html.Div(
                    id="chat-messages",
                    style={
                        "flex": "1",
                        "padding": "10px",
                        "overflowY": "auto",
                        "borderTop": "1px solid #333333",
                        "color": "#E0E0E0",  # Light text for messages
                        "display": "flex",
                        "flexDirection": "column",
                    },
                ),
                html.Div(
                    style={"padding": "10px", "display": "flex", "backgroundColor": "#1E1E1E"},
                    children=[
                        dbc.Input(
                            id="user-input",
                            placeholder="Message Course Recommender...",
                            type="text",
                            style={
                                "flex": "1",
                                "marginRight": "10px",
                                "backgroundColor": "#2C2C2C",
                                "color": "#FFFFFF",
                                "border": "1px solid #444",
                            },
                        ),
                        dbc.Button(
                            "Send",
                            id="send-button",
                            color="primary",
                            style={"backgroundColor": "#007BFF", "borderColor": "#007BFF"},
                        ),
                    ],
                ),
            ],
        ),
    ],
)

@app.callback(
    Output("chat-messages", "children"),
    Input("send-button", "n_clicks"),
    Input("user-input", "n_submit"),  # Capture Enter key submission
    State("user-input", "value"),
    State("course-dropdown", "value"),
    State("chat-messages", "children"),
    prevent_initial_call=True,
)
def update_chat(n_clicks, n_submit, user_message, selected_course, chat_messages):
    if not user_message or not selected_course:
        return chat_messages

    # Add user message (aligned to the right)
    chat_history = chat_messages or []
    chat_history.append(
        html.Div(
            f"{user_message}",
            style={
                "margin": "5px 0",
                "textAlign": "right",
                "color": "#FFFFFF",
                "backgroundColor": "#333333",
                "padding": "8px 12px",
                "borderRadius": "12px",
                "maxWidth": "70%",
                "alignSelf": "flex-end",
                "marginLeft": "auto",
            },
        )
    )

    try:
        response = requests.post(
            "http://127.0.0.1:5000/query",
            json={
                "question": user_message,
                "course_title": selected_course
            },
        )
        if response.status_code == 200:
            data = response.json()
            bot_reply = f"{data['answer']} (Confidence: {data['score']:.2f})"
        elif response.status_code == 404:
            bot_reply = "Course not found."
        else:
            bot_reply = "Error: Unable to process your request."
    except Exception as e:
        bot_reply = f"Error: {e}"

    chat_history.append(
        html.Div(
            f"{bot_reply}",
            style={
                "margin": "5px 0",
                "textAlign": "left",
                "color": "#FFFFFF",
                "backgroundColor": "#333333",
                "padding": "8px 12px",
                "borderRadius": "12px",
                "maxWidth": "70%",
                "alignSelf": "flex-start",
                "marginRight": "auto",
            },
        )
    )

    return chat_history

@app.callback(
    Output("user-input", "value"),
    Input("send-button", "n_clicks"),
    Input("user-input", "n_submit"),  # Clear input field when Enter is pressed
    prevent_initial_call=True,
)
def clear_input_field(n_clicks, n_submit):
    return ""
