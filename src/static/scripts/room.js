//import { WebsocketManager } from "./websocket_manager.js";


//const websockeAddress = "ws://10.1.73.49:4201";
//var websocket = new WebSocket(websockeAddress);

// var websocket = new WebSocket(websockeAddress);

// class WebsocketManager
// {
//     function
// }


// let websocketManager = new WebsocketManager("10.1.73.49", "4201", addToChatBox);


// async function joinRoomWithUsername()
// {
//     await websocketManager.sendWebsocketMessage({"type":"join", "room_id": room_id, "username": username});
// }

// async function sendChatMessage()
// {
//     console.log("clicked");
//     let message = $("#message-input").val();
//     if (!message.empty)
//     {
//         console.log(message);
//         await websocketManager.sendWebsocketMessage({"type":"chat_message", "room_id":room_id, "username":username, "message": message});

//         $("#message-input").val('');
//     }
// }

// function addToChatBox(message)
// {
//     $("#chat-box").append("<p>" + message + "</p>");
//     let bottomElement = $("chat-box").children[-1];
    
//     notificationAudio.play();
//     $("#chat-box").animate({scrollTop: 50000}, 500);
//     //$("#chat-box").scrollTop($("chat-box")[0].scrollHeight - $("chat-box")[0].clientHeight);
//     //$("#chat-box").scroll()
// }




function setupWebsocketConnection()
{
    websocket = new WebSocket(websockeAddress);
    
    console.log(websocket.readyState);
    websocket.addEventListener("message", ({ data }) => {
        console.log(data);
        const event = JSON.parse(data);
        //console.log(event["type"]);

        if (event.type ==  "player_joined")
        {
            console.log("Player Joined" + " with name" + event.username);
            addToChatBox("Player joined: " + event.username);
            
            //$("#chat-box").append("<p>Player joined: " + event.username+"</p>");

            //$("#players-list").append('<ul id="' + event.username+'">' + event.username + "</ul>");

        }

        if (event.type == "user_disconnect")
        {
            // var useritem = ("#"+event.username);
            // console.log(useritem);
            // $(useritem).remove();
        }

        if (event.type == "game_update")
        {

        }

        if (event.type == "room_update")
        {
            let roomData = event.room_data
            $("#players-list").empty();
            console.log($("#players-list").children.length)

            for (let i = 0; i < roomData.connected_users.length; i++)
            {
                $("#players-list").append('<li>' + roomData.connected_users[i] + "</li>");
            }
        }

        if (event.type == "chat_message")
        {
            addToChatBox(event.username + ": " + event.message);
            //$("#chat-box").append("<p>" + event.username + ": " + event.message + "</p>");
        }

        // switch (event.type)
        // {
        //     case "player_joined":
        //         console.log("Player Joined" + " with name" + event.username);
        //         $("#chat-box").append("<p>Player joined: " + event.username+"</p>");
        //         $("#players-list").append('<ul id="' + event.username+'">' + event.username + "</ul>");

        //     case "user_disconnect":
        //         var useritem = ("#"+event.username);
        //         console.log(useritem);
        //         $(useritem).remove();
        //     case "game_update":
        //         //$()
        //         console.log("");
        // }

    // do something with event
    });

    //websocket.send(JSON.stringify({"type":"join", "room_id": room_id, "username": username}));
}
function updateGame()
{
    //$()
}

async function sendWebsocketMessage(message)
{
    if (websocket.readyState == websocket.OPEN)
    {
        await sleep(1000 * .25);
        websocket.send(JSON.stringify(message));
    }
    else if (websocket.readyState == websocket.CONNECTING)
    {
        await sleep(1000 * .25);
        console.log(websocket.readyState);
        await sendWebsocketMessage(message);
        
    }
    else if (websocket.readyState == websocket.CLOSED)
    {
        await sleep(1000 * 0.25);
        console.log(websocket.readyState);
        setupWebsocketConnection();
        await sendWebsocketMessage(message);
    }
}


// async function joinRoomWithUsername()
// {
//     await sendWebsocketMessage({"type":"join", "room_id": room_id, "username": username});
// }


// async function sendChatMessage()
// {
//     console.log("clicked");
//     let message = $("#message-input").val();
//     if (!message.empty)
//     {
//         console.log(message);
//         await sendWebsocketMessage({"type":"chat_message", "room_id":room_id, "username":username, "message": message});

//         $("#message-input").val('');
//     }
// }

// function addToChatBox(message)
// {
//     $("#chat-box").append("<p>" + message + "</p>");
//     let bottomElement = $("chat-box").children[-1];
    
//     notificationAudio.play();
//     $("#chat-box").animate({scrollTop: 50000}, 500);
//     //$("#chat-box").scrollTop($("chat-box")[0].scrollHeight - $("chat-box")[0].clientHeight);
//     //$("#chat-box").scroll()
// }


const sleep = (delay) => new Promise((resolve) => setTimeout(resolve, delay))

// async function joinRoomWithUsername()
// {
//     if (websocket.readyState == websocket.OPEN)
//     {
//         await sleep(1000 * .25);
//         websocket.send(JSON.stringify({"type":"join", "room_id": room_id, "username": username}));
//     }
//     else if (websocket.readyState == websocket.CONNECTING)
//     {
//         await sleep(1000 * .25);
//         console.log(websocket.readyState);
//         await joinRoomWithUsername();
        
//     }
//     else if (websocket.readyState == websocket.CLOSED)
//     {
//         await sleep(1000 * 0.25);
//         console.log(websocket.readyState);
//         setupWebsocketConnection();
//         await joinRoomWithUsername();
//     }
// }


//$("#game-canvas")