const sleep = (delay) => new Promise((resolve) => setTimeout(resolve, delay))

class WebsocketManager
{
    constructor (address, port, chatMessageCallback, updatePlayersCallback)
    {
        let fullAddress = "ws://" + address + ":" + port;

        this.websocket = new WebSocket(fullAddress);
        
        this.websocket.addEventListener("message", ({data}) => this.handleSocketComms(data));

        this.chatMessageCallback = chatMessageCallback;
        this.updatePlayersCallback = updatePlayersCallback;
    }

    handleSocketComms(data)
    {
        console.log(data);
        const event = JSON.parse(data);

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
                console.log(event.table)
                for (var i = 0; i < event.table.seats.length; i++)
                {
                    if (event.table.seats[i].player != null)
                    {
                        console.log(event.table.seats[i]);
                    }
                }
            }
    
            if (event.type == "room_update")
            {
                this.updatePlayersCallback(event.room_data);
            }
    
            if (event.type == "chat_message")
            {
                this.chatMessageCallback(event.username + ": " + event.message);
            }    
    }



    async sendWebsocketMessage(message)
    {
        console.log("SENDING WEBSOCKET MESSAGE");
        if (this.websocket.readyState == this.websocket.OPEN)
        {
            await sleep(1000 * .25);
            this.websocket.send(JSON.stringify(message));
        }
        else if (this.websocket.readyState == this.websocket.CONNECTING)
        {
            await sleep(1000 * .25);
            console.log(this.websocket.readyState);
            await this.sendWebsocketMessage(message);
            
        }
        else if (this.websocket.readyState == this.websocket.CLOSED)
        {
            await sleep(1000 * 0.25);
            console.log(this.websocket.readyState);
            this.setupWebsocketConnection();
            await this.sendWebsocketMessage(message);
        }
    }


    async joinRoomWithUsername()
    {
        await this.sendWebsocketMessage({"type":"join", "room_id": room_id, "username": username});
    }

    async requestSeat()
    {
        await this.sendWebsocketMessage({"type": "request_seat", "room_id": room_id, "username": username});
    }
}