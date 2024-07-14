
const boardAtlasData = {
    frames: {
        card1: {
            frame: { x: 0, y:0, w:88, h:124 },
        },

    },
    meta: {
        image: "{{ url_for('static', filename='images/Cards/diamonds.png')}}",
        format: 'RGBA8888',
        size: { w: 352, h: 372 },
        scale: 2
    },
    animations: {
        enemy: ['card1'] //array of frames by name
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
        enemy: ['card1'] //array of frames by name
    }
}
