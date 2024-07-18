
const cardFrames = {
    ace: {
        frame: { x: 0, y:0, w:88, h:124 },
    },
    two: {
        frame: { x: (88*1), y:0, w:88, h:124 },
    },
    three: {
        frame: { x: (88*2), y:0, w:88, h:124 },
    },
    four: {
        frame: { x: (88*3), y:0, w:88, h:124 },
    },
    five: {
        frame: { x: (88*4), y:0, w:88, h:124 },
    },
    six: {
        frame: { x: 0, y:124, w:88, h:124 },
    },
    seven: {
        frame: { x: (88*1), y:124, w:88, h:124 },
    },
    eight: {
        frame: { x: (88*2), y:124, w:88, h:124 },
    },
    nine: {
        frame: { x: (88*3), y:124, w:88, h:124 },
    },
    ten: {
        frame: { x: (88*4), y:124, w:88, h:124 },
    },
    jack: {
        frame: { x: 0, y:(124*2), w:88, h:124 },
    },
    king: {
        frame: { x: (88*1), y:(124*2), w:88, h:124 },
    },
    queen: {
        frame: { x: (88*2), y:(124*2), w:88, h:124 },
    },

}


const chipsAtlasData = {
    frames: {
        white: {
            frame: {x: 0, y:0, w:64, h:72}
        },
        red: {
            frame: {x: 64*1, y:0, w:64, h:72}
        },
        green: {
            frame: {x: 64*2, y:0, w:64, h:72}
        },
        blue: {
            frame: {x: 64*3, y:0, w:64, h:72}
        },
        black: {
            frame: {x: 64*4, y:0, w:64, h:72}
        },
        yellow: {
            frame: {x: 0, y:72, w:64, h:72}
        },
        orange: {
            frame: {x: 64*1, y:72, w:64, h:72}
        },
        purple: {
            frame: {x: 64*2, y:72, w:64, h:72}
        },
        pink: {
            frame: {x: 64*3, y:72, w:64, h:72}
        },
        brown: {
            frame: {x: 64*4, y:72, w:64, h:72}
        },

    },
    meta: {
        image: "/images/Chips/chips.png",
        format: 'RGBA8888',
        size: { w: 320, h: 144 },
        scale: 1
    },
    animations: {
        chips: ['white', 'red', 'green', 'blue', 'black', 'yellow', 'orange', 'purple', 'pink', 'brown']
    }
}

const spadesAtlasData = {
    frames: cardFrames,
    meta: {
        image: "/images/Cards/spades.png",
        format: 'RGBA8888',
        size: { w: 352, h: 372 },
        scale: 1
    },
    animations: {
        cards: ['ace', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'jack', 'king', 'queen'], //array of frames by name
    }
}

const clubsAtlasData = {
    frames: cardFrames,
    meta: {
        image: "/images/Cards/clubs.png",
        format: 'RGBA8888',
        size: { w: 352, h: 372 },
        scale: 1
    },
    animations: {
        cards: ['ace', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'jack', 'king', 'queen'], //array of frames by name
    }
}

const diamondsAtlasData = {
    frames: cardFrames,
    meta: {
        image: "/images/Cards/diamonds.png",
        format: 'RGBA8888',
        size: { w: 352, h: 372 },
        scale: 1
    },
    animations: {
        cards: ['ace', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'jack', 'king', 'queen'], //array of frames by name
    }
}

const heartsAtlasData = {
    frames: cardFrames,
    meta: {
        image: "/images/Cards/hearts.png",
        format: 'RGBA8888',
        size: { w: 352, h: 372 },
        scale: 1
    },
    animations: {
        cards: ['ace', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'jack', 'king', 'queen'], //array of frames by name
    }
}


const playerLocations = [

    {
        x: 60, y: 70
    },
    {
        x: 10, y: 185
    },
    {
        x: 60, y: 310
    },
    {
        x: 530, y: 310
    },
    {
        x: 580, y: 185
    },
    {
        x: 530, y: 70
    },
]

function getFrameFromValue(cardVal)
{
    switch (cardVal)
    {
        case "A":
            return 0;
        case "2":
            return 1;
        case "3":
            return 2;
        case "4":
            return 3;
        case "5":
            return 4;
        case "6":
            return 5;
        case "7":
            return 6;
        case "8":
            return 7;
        case "9":
            return 8;
        case "10":
            return 9;
        case "J":
            return 10;
        case "K":
            return 11;
        case "Q":
            return 12;
    }
}

function getChipFromValue(chipVal)
{
    switch (chipVal)
    {
        //TODO: Implementation
        case 10:
            return null;
    }
}