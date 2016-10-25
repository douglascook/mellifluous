import Html exposing (Html, Attribute, div, input, button, text)
import Html.App as App
import Html.Attributes exposing (..)
import Html.Events exposing (onInput, onClick)

import String


main =
  App.program
    { init = init,
      view = view,
      update = update,
      subscriptions = subscriptions
    }


-- MODEL

type alias Model =
  { username : String,
    password : String }

model : Model
model =
  Model "" ""


-- INIT

init: (Model, Cmd Msg)
init =
  (model, Cmd.none)


-- UPDATE

type Msg =
  Username String |
  Password String |
  Submit

update : Msg -> Model -> (Model, Cmd Msg)
update msg model =
  case msg of
    Username username  ->
      ( { model | username = username }, Cmd.none )

    Password password ->
      ( { model | password = password }, Cmd.none )

    Submit ->
      ( { model | password = "noooooooooo"}, Cmd.none )


-- SUBSCRIPTIONS


subscriptions : Model -> Sub Msg
subscriptions model =
  Sub.none


-- VIEW

view: Model -> Html Msg
view model =
  div [] [
    div [] [ input [placeholder "Username", onInput Username] [] ],
    div [] [ input [placeholder "Password", onInput Password] [] ],
    div [] [ text (toString model.password) ],
    button [ onClick Submit ] [ text "Log in" ]
  ]
