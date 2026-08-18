import React from "react"
import {createBrowserRouter} from "react-router-dom"
import Formularz from "./layouts/MainPage"

export const router = createBrowserRouter([
    {
        path: "/",
        element: <Formularz/>,
    },
])