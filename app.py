'''
THIS IS THE MAIN PROGRAM -- Frontend

TODO:// Moving all of the functions from the instafuncts python file to this one, Poor structure but it's easier to build
 - Move comment all button to this
 - Include the tutorial page
 - Pickle the driver variables
 - store username in DCC
 - pickle name needs to be the username :)
 - that means you can have a single account open once. idk if this will work on the driver tho...
'''

import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from instaFuncs import *
from instaConsts import *

try:
    from selenium import webdriver
    import time
    import random
    import pickle
except:
    pass

# GLOBAL DRIVER VARIABLE
# Driver is stored as a pickled object... This means there can only be one person operating the server at any given time
# :( proper proper sad...
# The goal

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server
#
#
#   Homepage
#
#

follow_new_users_collapse = html.Div(
    [
        dbc.Button(
            "Follow New Users",
            id="collapse-button",
            className="mb-3",
            color="primary",
        ),
        dbc.Collapse(
            dbc.Card(
                [dbc.CardBody([
                    html.P("Enter in the users separated by a space"),
                    dbc.FormGroup(
                        [
                            dbc.Label("Popular Users"),
                            dbc.Input(placeholder="Users goes here...", type="text", id='follow_users_text'),
                            dbc.FormText("Enter popular users in your niche"),
                            dbc.Label("Follow from posts or users?"),
                            dbc.RadioItems(
                                options=[
                                    {"label": "Recent Posts", "value": 1},
                                    {"label": "Recent Follows", "value": 2},
                                ],
                                value=1,
                                id="follow-new-users-input",
                            ),
                        ]
                    ),
                    dbc.Button(
                        "Run",
                        id="follow-new-users-button",
                        className="mb-3",
                        color="primary",
                    ),
                    html.Div(id="follow-new-users-alert", style={'height': '10%'}),
                ]
                )
                ]
            ),
            id="collapse",
        ),
    ]
)

unfollow_all_users_collapse = html.Div(
    [
        dbc.Button(
            "Unfollow All Users",
            id="collapse-button-1",
            className="mb-3",
            color="primary",
        ),
        dbc.Collapse(
            dbc.Card(
                [dbc.CardBody([
                    html.P("Firstly, enter your username. Then select a type."),
                    dbc.FormGroup(
                        [
                            dbc.Label("Username"),
                            dbc.Input(placeholder="Your username", type="text", id='your_username_text'),
                            dbc.FormText("Make sure it's your username or else..."),
                            dbc.Label("Unfollow users:"),
                            dbc.RadioItems(
                                options=[
                                    {"label": "All Users", "value": 1},
                                    {"label": "Users Not Following You", "value": 2},
                                ],
                                value=1,
                                id="unfollow-users-type-input",
                            ),
                        ]
                    ),
                    dbc.Button(
                        "Run",
                        id="unfollow-users-button",
                        className="mb-3",
                        color="primary",
                    ),
                    html.Div(id="unfollow-users-alert", style={'height': '10%'}),
                ]
                )
                ]
            ),
            id="collapse-1",
        ),
    ]
)

buttons = dbc.Card(
    dbc.CardBody(
        [
            html.H5("Actions", className="card-title"),
            html.P(
                "Press the actions you'd like the program to run..."
            ),
            follow_new_users_collapse,
            unfollow_all_users_collapse,
            dbc.Button("Message All Users", color="danger", style={'marginTop': '2%', 'marginBottom': '2%'}),
        ],
        style={'marginTop': '2%', 'marginBottom': '2%'}
    )
)

text = [
    "Select an action to begin, you can wait until the action is finished (recommended) or you can kill the action and try again..."]

console_log = dbc.Card(
    dbc.CardBody(
        [
            html.H5("Console Log", className="card-title"),
            dbc.Row(
                children=[
                    html.P(
                        "Checkout the output log",
                        style={'marginLeft': 1, 'marginRight': '5%'}
                    ),
                    dbc.Button("Kill", color="danger"),
                ],
                style={
                    'paddingLeft': '3%', 'marginBottom': '5%'
                }
            ),
            html.Div(children=html.Code(array_to_string(text), id='console-log'),
                     style={'height': 190, 'overflow': 'scroll', 'backgroundColor': '#dbdbdb', 'borderRadius': 7,
                            'padding': 5})
        ]
    ),
    style={
        'height': 350,
        "white-space": "pre-line"
    }
)

main_area = dbc.Row([dbc.Col(buttons, width=4), dbc.Col([dcc.Interval(
    id='interval-component',
    interval=1 * 1000,  # in milliseconds
    n_intervals=0
), console_log], width=8)], style={'marginTop': '5%'})

home_page_layout = html.Div(
    [
        dbc.Row(
            children=[
                dbc.Card(
                    dbc.CardBody(
                        [
                            html.H5("Login Details", className="card-title"),
                            dbc.Input(id="username", placeholder="Username...", type="text",
                                      style={'marginTop': '10%', 'marginBottom': '10%'}),
                            dbc.Input(id="password", placeholder="Password...", type="text",
                                      style={'marginTop': '10%', 'marginBottom': '10%'}),
                            dbc.Button("Start Server", id='start-server', color="primary", className="mr-1"),
                            html.Div(id='server-status')
                        ]
                    ),
                    style={'width': '30%', 'marginRight': '5%'}
                ),
                dbc.Card(
                    dbc.CardBody(
                        [
                            html.H5("System Requirements", className="card-title"),
                            html.P(
                                [
                                    "Make sure to follow the tutorial, to get the program up and running",
                                ],
                                className="card-text",
                            ),
                            html.P(
                                [
                                    "You need to have: ", html.Code("selenium, time, and random")
                                ],
                                className="card-text",
                            ),
                            html.P(
                                [
                                    "Don't press any links after running a command",
                                ],
                                className="card-text",
                            ),
                            dbc.Row(
                                children=[
                                    dbc.Button("Test Requirements", id="test-requirements", color="primary",
                                               style={'height': '15%', 'marginLeft': '5%', 'marginRight': '5%'}),
                                    html.Div(id="test-alert", style={'height': '10%'}),
                                ],
                            )
                        ]
                    ),
                    style={'width': '60%'}
                ),
                main_area
            ],
            style={'marginLeft': 'auto', 'marginRight': 'auto', 'width': '80%', 'paddingTop': '5%',
                   'alignContent': 'center'}
        )

    ]
)

#
#
# Error Page
#
#
error_container = html.Div(children=[dbc.Card(
    [
        dbc.CardBody(
            [
                html.H4("Error 404 - Page Not Found", className="card-title"),
                html.P(
                    "The page you requested doesn't exist... ",
                    className="card-text",
                ),
                html.P(
                    "This is a little bit crazy because there literally aren't any extra links to click...",
                    className="card-text",
                ),
                html.P(
                    "Congrats! You're another level of stupid!!",
                    className="card-text",
                ),
            ],
        ),

    ],
    style={"width": "25rem", 'marginLeft': 'auto', 'marginRight': 'auto', },
)], style={'paddingTop': '15%'})

error_layout = html.Div(children=error_container,
                        className='container',
                        style={'background-color': 'rgba(255, 117, 117, 0.5)',
                               'height': 700, 'justifyContent': 'center', 'alignItems': 'center'})

#
#
# Help Page
#
#

help_container = html.Div(children=[dbc.Card(
    [
        dbc.CardBody(
            [
                html.H4("Contact Me", className="card-title"),
                html.P(
                    "Email: aa1719@ic.ac.uk ",
                    className="card-text",
                    style={'text-align': 'center'}
                ),
                html.P(
                    "Instagram: @ElijahAhmad__",
                    className="card-text",
                    style={'text-align': 'center'}
                ),
                html.P(
                    "Snapchat: @elijah.ahmad",
                    className="card-text",
                    style={'text-align': 'center'}
                ),
            ],
        ),

    ],
    style={"width": "25rem", 'marginLeft': 'auto', 'marginRight': 'auto', },
)], style={'paddingTop': '15%'})

help_layout = html.Div(children=help_container,
                       className='container',
                       style={'background-color': 'rgba(207, 255, 248, 0.5)',
                              'height': 700, 'justifyContent': 'center', 'alignItems': 'center'})

#
#
# Heading + Navigation
#

heading = html.Div(
    children=([
        html.Div(
            children=[
                html.H1(
                    children='InstaMation',
                    style={
                        'width': '100%',
                        'height': '70%',
                        'overflow': 'visible',
                        'fontFamily': '"Open sans", sans-serif',
                        'color': "#463249",
                        'fontSize': 25,
                        'textAlign': 'center',
                        'fontWeight': 400,
                        'marginTop': '3%',
                        'marginBottom': 'auto',

                    }
                ),
                html.P(
                    children='Making Instagram Automation Easier',
                    style={
                        'width': '100%',
                        'height': '70%',
                        'overflow': 'visible',
                        'fontFamily': '"Open Sans", sans-serif',
                        'color': "#793466",
                        'fontSize': 18,
                        'textAlign': 'center',
                        'fontWeight': 300,
                        'margin': 10
                    }
                )]
        )

    ]),
    style={
        'height': '30%',
        'width': '100%',
        'flex': 1,
        'justifyContent': 'center',
        'alignItems': 'center',
    },
)

navigationBar = html.Div(
    children=(
        dbc.Row(children=[
            dcc.Link('Tutorial', href='/tutorial', style={'marginRight': '10%', 'color': '#474747'}),
            dcc.Link('Home', href='/', style={'marginHorizontal': '2%', 'color': '#474747'}),
            dcc.Link('Help', href='/help', style={'marginLeft': '10%', 'color': '#474747'}),
        ],
            className="justify-content-center align-items-center")
    ),
    style={
        'height': '5%',
        'width': '100%',
        'backgroundColor': 'rgba(255, 209, 247, 0.34)',
        'marginTop': '2%'
    }
)

#
#
#
#

app.layout = html.Div([
    # represents the URL bar, doesn't render anything
    dcc.Location(id='url', refresh=False),
    # content will be rendered in this element
    heading,
    navigationBar,
    html.Div(id='page-content')
])

home_layout = html.Div(children=[home_page_layout],
                       className='container',
                       style={'background-color': 'rgba(239, 230, 239, 0.5)',
                              'height': 1000})


@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/':
        return home_layout
    elif pathname == '/help':
        return help_layout
    else:
        return error_layout


@app.callback(
    dash.dependencies.Output("test-alert", "children"), [dash.dependencies.Input("test-requirements", "n_clicks")]
)
def on_button_click(n):
    if n == None:
        return ''
    testArray = ['selenium', 'time', 'random']
    # test selinium
    try:
        from selenium import webdriver
        testArray[0] = ''
    except ImportError as e:
        pass
    # test time
    try:
        import time
        testArray[1] = ''
    except ImportError as e:
        pass

    # test random
    try:
        import random
        testArray[2] = ''
    except ImportError as e:
        pass

    stringoftests = testArray[0] + ' ' + testArray[1] + ' ' + testArray[2]

    if (len(stringoftests) > 2):
        return dbc.Alert(children=("Error! Install: " + stringoftests), color="danger", style={'height': '10%'})

    return dbc.Alert(children="All Requirements are up-to-date!", color="success", style={'height': '10%'})


@app.callback(
    dash.dependencies.Output('server-status', 'children'),
    [dash.dependencies.Input("start-server", "n_clicks"),
     dash.dependencies.Input('username', 'value'),
     dash.dependencies.Input('password', 'value')
     ]
)
def start_server(n, username, password):
    if n == None:
        return None
    try:
        text.append('Attempting Login:  ' + username)
        driver = start_up(username, password)
        with open('driver.pickle', 'wb') as f:
            pickle.dump(driver, f)
        text.append('logged in as user: ' + username)
        text.append('logged in Successful!')
        return dbc.Alert(children="Logged in Success", color='success', style={'marginTop': 10})
    except:
        return dbc.Alert(children="Login Failed...", color='danger', style={'marginTop': 10})


@app.callback(
    dash.dependencies.Output('follow-new-users-alert', 'children'),
    [
        dash.dependencies.Input('follow-new-users-button', 'n_clicks'),
        dash.dependencies.Input('follow-new-users-input', 'value'),
        dash.dependencies.Input('follow_users_text', 'value'),
    ]
)
def follow_new_users(n, method, users):
    if n == None:
        return None
    user_array = users.split()
    with open("driver.pickle", 'rb') as f:
        driver = pickle.load(f)
    if method == 1:
        # follow posts
        try:
            count = 0
            while count < len(user_array):
                for i in user_array:
                    # collect the usernames that you need to follow
                    go_to_page(i, driver)
                    text.append('At ' + i + 's page')
                    sleep_random_decimals(2, 4)
                    try:
                        first_post = driver.find_element_by_xpath(first_post_xpath1)
                    except:
                        try:
                            first_post = driver.find_element_by_xpath(first_post_xpath2)
                        except:
                            text.append("Could not find the first post <-- Serious Error, report to Eli")
                            text.append('moving on to next user')
                            continue

                    first_post.location_once_scrolled_into_view
                    sleep_random_decimals(2, 4)
                    first_post.click()
                    sleep_random_decimals(2, 4)

                    try:
                        bars = driver.find_element_by_xpath(bar_xpath)
                        bars.location_once_scrolled_into_view
                        likes = driver.find_element_by_xpath(liked_by_xpath)
                        sleep_random_decimals(2, 4)
                    except:
                        text.append('The first post was probably a video, moving on...')
                        continue
                    sleep_random_decimals(1, 2)
                    likes.click()
                    sleep_random_decimals(2, 4)
                    for j in range(1, random.randint(10, 50)):
                        try:
                            new_username = driver.find_element_by_xpath(
                                username_from_list(j))
                            follow_button = driver.find_element_by_xpath(
                                follow_button_from_list(j))

                            if follow_button.text == "Follow":
                                new_username_text = new_username.text
                                follow_button.click()
                                text.append("following:\t" + new_username_text)
                            else:
                                text.append("Already Following: \t" + new_username.text)
                            # Make a database of users to follow
                            sleep_random_decimals(30, 50)
                            follow_button.location_once_scrolled_into_view
                        except:
                            text.append("Unable to Follow Users --> If persists, message Elijah")
                    # sleep randomly inbetween getting users to reduce the suspicion of instagram
                    sleep_random_decimals(60, 120)
                count += 1
            return dbc.Alert(children="Success!", color='success', style={'marginTop': 10})
        except:
            text.append('Program Follow Function Failed, send screenshot to Eli')
            return dbc.Alert(children="Failed", color='danger', style={'marginTop': 10})
    elif method == 2:
        try:
            try:
                count = 0
                while count < len(user_array):
                    for i in user_array:
                        # collect the usernames that you need to follow
                        go_to_page(i, driver)
                        text.append('At ' + i + 's page')
                        sleep_random_decimals(4, 6)

                        try:
                            follow_button = driver.find_element_by_xpath(followers_button_xpath)
                            follow_button.location_once_scrolled_into_view
                            follow_button.click()
                        except:
                            text.append("Could not click on the followers button <--")
                            continue

                        sleep(5)

                        for j in range(2, random.randint(10, 50)):
                            try:
                                try:
                                    # print(username_from_followers_list(j))
                                    new_username = driver.find_element_by_xpath(
                                        username_from_followers_list(j))
                                except:
                                    text.append('Could not get username button...')

                                try:
                                    # print(follow_button_from_followers_list(j))
                                    follow_button = driver.find_element_by_xpath(
                                        follow_button_from_followers_list(j))
                                except:
                                    text.append('Could not get follow button...')
                                    continue

                                if follow_button.text == "Follow":
                                    new_username_text = new_username.text
                                    follow_button.click()
                                    text.append("following:\t" + new_username_text)
                                else:
                                    text.append("Already Following: \t" + new_username.text)
                                # Make a database of users to follow
                                sleep_random_decimals(30, 50)
                                follow_button.location_once_scrolled_into_view
                            except:
                                text.append("Unable to Follow Users --> If persists, message Elijah")
                        # sleep randomly inbetween getting users to reduce the suspicion of instagram
                        sleep_random_decimals(60, 120)
                    count += 1

                return dbc.Alert(children="Success!", color='success', style={'marginTop': 10})
            except:
                text.append('Program Follow Function Failed, send screenshot to Eli')
                return dbc.Alert(children="Failed", color='danger', style={'marginTop': 10})
        except:
            return dbc.Alert(children="Failed", color='danger', style={'marginTop': 10})


@app.callback(
    dash.dependencies.Output('unfollow-users-alert', 'children'),
    [
        dash.dependencies.Input('unfollow-users-button', 'n_clicks'),
        dash.dependencies.Input('unfollow-users-type-input', 'value'),
        dash.dependencies.Input('your_username_text', 'value')
    ]
)
def unfollow_users(n, method, username):
    if n == None:
        return None
    with open("driver.pickle", 'rb') as f:
        driver = pickle.load(f)
    if method == 1:
        # follow posts
        try:
            try:
                go_to_page(username, driver)
                text.append('At ' + username + 's page')
                sleep(2)
                try:
                    following_button = driver.find_element_by_xpath(following_button_xpath)
                    following_number = int(driver.find_element_by_xpath(following_number_xpath).text.replace(',', ''))
                    text.append('Following : ' + str(following_number))
                    sleep(2)
                    following_button.click()
                    sleep(2)
                    try:
                        count = 1
                        error = 0
                        print(following_number)
                        while count <= (following_number + 1) and error < 10:
                            try:
                                new_username_tag = driver.find_element_by_xpath(username_from_unfollowing_list(count))
                                new_username = new_username_tag.text
                                error = 0
                            except:
                                text.append('failed to find the new username')
                                count=following_number+1
                                error += 1
                                continue

                            print(new_username)
                            try:
                                unfollow_button = driver.find_element_by_xpath(
                                    unfollow_button_from_unfollowing_list(count))
                            except:
                                text.append('failed to find the unfollow button')
                                count = following_number + 1
                                continue

                            unfollow_button.click()
                            try:
                                confirm_button = driver.find_element_by_xpath(confirm_unfollow_button)
                                confirm_button.click()
                            except:
                                print('user did not have a confirm unfollow button')
                            text.append('Unfollowed: ' + new_username)
                            new_username_tag.location_once_scrolled_into_view

                            sleep_random_decimals(20, 40)
                            count = count + 1

                        if (error == 10):
                            text.append('Failed to find username 10 times in a row. Error.')

                        return dbc.Alert(children="Success!", color='success', style={'marginTop': 10})
                    except:
                        text.append('failed to get the following')
                        return dbc.Alert(children="Failed", color='danger', style={'marginTop': 10})
                except:
                    text.append('unable to click the following button')
                    return dbc.Alert(children="Failed", color='danger', style={'marginTop': 10})
            except:
                text.append('Unable to travel to your page, check username.')
                return dbc.Alert(children="Failed", color='danger', style={'marginTop': 10})

        except:
            text.append('Program Unfollow Function Failed, send screenshot to Eli')
            return dbc.Alert(children="Failed", color='danger', style={'marginTop': 10})
    elif method == 2:
        try:
            return dbc.Alert(children="Success!", color='success', style={'marginTop': 10})
        except:
            text.append('Program Unfollow Function Failed, send screenshot to Eli')
            return dbc.Alert(children="Failed", color='danger', style={'marginTop': 10})


@app.callback(
    dash.dependencies.Output("collapse", "is_open"),
    [dash.dependencies.Input("collapse-button", "n_clicks")],
    [dash.dependencies.State("collapse", "is_open")],
)
def toggle_collapse1(n, is_open):
    if n:
        return not is_open
    return is_open


@app.callback(
    dash.dependencies.Output("collapse-1", "is_open"),
    [dash.dependencies.Input("collapse-button-1", "n_clicks")],
    [dash.dependencies.State("collapse-1", "is_open")],
)
def toggle_collapse2(n, is_open):
    if n:
        return not is_open
    return is_open


@app.callback(dash.dependencies.Output('console-log', 'children'),
              [dash.dependencies.Input('interval-component', 'n_intervals')])
def update_console_log(n):
    return array_to_string(text)

server.secret_key = os.environ.get('SECRET_KEY', 'default-value-used-in-development')
app.title = 'Instamation'

if __name__ == '__main__':
    app.run_server(debug=False, port=8080, host="0.0.0.0")
