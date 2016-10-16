import Html exposing (Html, Attribute, div, input, text)
import Html.App as App
import Html.Attributes exposing (..)
import Html.Events exposing (onInput)

import String


main =
  App.beginnerProgram { model = model, view = view, update = update }


-- MODEL

type alias Model =
  { username : String,
    password : String }

model : Model
model =
  { username = "",
    password = "" }


-- UPDATE

type Msg =
  Username String |
  Password String

update : Msg -> Model -> Model
update msg model =
  case msg of
    Username username  ->
      { model | username = username }

    Password password ->
      { model | password = password }


-- VIEW

view: Model -> Html Msg
view model =
  div [] [
    div [] [ input [placeholder "Username", onInput Username] [] ],
    div [] [ input [placeholder "Password", onInput Password] [] ]
  ]
