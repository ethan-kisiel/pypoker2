
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
        frame: { x: (88*1), y:0, w:88, h:124 },
    },
    queen: {
        frame: { x: (88*2), y:0, w:88, h:124 },
    },

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
        image: "/images/Cards/diamonds.png",
        format: 'RGBA8888',
        size: { w: 352, h: 372 },
        scale: 1
    },
    animations: {
        cards: ['ace', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'jack', 'king', 'queen'], //array of frames by name
    }
}

const handAtlasData = {
    frames: {
        card1: {
            frame: { x: 0, y:0, w:88, h:124 },
        },

    },
    meta: {
        image: "/images/Cards/diamonds.png",
        format: 'RGBA8888',
        size: { w: 352, h: 372 },
        scale: 1
    },
    animations: {
        a: ['a'] //array of frames by name
    }
}
