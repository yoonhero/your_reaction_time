import {useEffect, useRef, useState} from "react"
import {useRouter} from "next/router"
import {E, connect, updateState} from "/utils/state"
import "focus-visible/dist/focus-visible"
import {Button, Center, Text, VStack} from "@chakra-ui/react"
import NextHead from "next/head"

const EVENT = "ws://localhost:8000/event"
export default function Component() {
const [state, setState] = useState({"con": false, "finish_game": true, "game_start": 0, "game_start_time": null, "score": 0, "stop": false, "events": [{"name": "state.hydrate"}]})
const [result, setResult] = useState({"state": null, "events": [], "processing": false})
const router = useRouter()
const socket = useRef(null)
const { isReady } = router;
const Event = events => setState({
  ...state,
  events: [...state.events, ...events],
})
useEffect(() => {
  if(!isReady)
    return;
  if (!socket.current) {
    connect(socket, state, result, setResult, router, EVENT)
  }
  const update = async () => {
    if (result.state != null) {
      setState({
        ...result.state,
        events: [...state.events, ...result.events],
      })
      setResult({
        state: null,
        events: [],
        processing: false,
      })
    }
    await updateState(state, result, setResult, router, socket.current)
  }
  update()
})
return (
<Center sx={{"width": "100%", "height": "100vh"}}>
{state.finish_game ? <VStack>
<Text sx={{"fontSize": "60px"}}>
{`Are You Ready?`}</Text>
<Button onClick={() => Event([E("state.start_game", {})])}
sx={{"bg": "#8DCBE6", "color": "#F7F5EB", "fontSize": "30px", "padding": "20px"}}>
{`Yes`}</Button></VStack> : state.con ? <Center sx={{"width": "100%", "height": "100%"}}>
{state.stop ? <VStack>
<Text sx={{"fontSize": "200px"}}>
{(state.score + "ms")}</Text>
<Button onClick={() => Event([E("state.restart", {})])}>
{`restart`}</Button></VStack> : <Button isActive={true}
onClick={() => Event([E("state.stop_timer", {})])}
sx={{"width": "100%", "height": "100%"}}>
<Text sx={{"fontSize": "50px", "color": "#86C8BC"}}>
{`Click!`}</Text></Button>}</Center> : <Center sx={{"width": "100%", "height": "100%"}}>
<Text sx={{"fontSize": "50px"}}>
{`Click When Text Gets Green!`}</Text></Center>}
<NextHead>
<title>{`Pynecone App`}</title>
<meta content="A Pynecone app."
name="description"/>
<meta property="og:image"
content="favicon.ico"/></NextHead></Center>
)
}