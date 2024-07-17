
console.log(1)

const app = new PIXI.Application();

app.init({ width: 800, height: 600,
    view: document.getElementById("game-canvas"),
    backgroundColor: "#858163",
    antialias: true,
});
//app.setCanvas(document.getElementById("game-canvas"));
//document.body.appendChild(app.canvas);


PIXI.Assets.load("/images/table.png");

let sprite = PIXI.Sprite.from("/images/table.png");

console.log(sprite);

app.stage.addChild(sprite);

await PIXI.Assets.load("{{ url_for('static', filename='images/Cards/diamonds.png')}}")
await PIXI.Assets.load("{{ url_for('static', filename='images/Cards/hearts.png')}}")
await PIXI.Assets.load("{{ url_for('static', filename='images/Cards/spades.png')}}")
await PIXI.Assets.load("{{ url_for('static', filename='images/Cards/clubs.png')}}")

console.log(heartsAtlasData);
const heartsSS = new PIXI.Spritesheet(PIXI.Texture.from(heartsAtlasData.meta.image), heartsAtlasData);
const diamondsSS = new PIXI.Spritesheet(PIXI.Texture.from(diamondsAtlasData.meta.image), diamondsAtlasData);
const clubsSS = new PIXI.Spritesheet(PIXI.Texture.from(clubsAtlasData.meta.image), clubsAtlasData);
const spadesSS = new PIXI.Spritesheet(PIXI.Texture.from(spadesAtlasData.meta.image), spadesAtlasData);
// load the fonts
await PIXI.Assets.load('/fonts/Helvetica.ttf');


//console.log(atlasData);
//const handSpritesheet = new PIXI.Spritesheet(PIXI.Texture.from(handAtlasData.meta.image), handAtlasData);

await heartsSS.parse();
await diamondsSS.parse();
await clubsSS.parse();
await spadesSS.parse();

//await handSpritesheet.parse();

//const handCard1 = new PIXI.AnimatedSprite(handSpritesheet.animations.enemy);

const card1 = new PIXI.AnimatedSprite(heartsSS.animations.cards);
const card2 = new PIXI.AnimatedSprite(diamondsSS.animations.cards);
const card3 = new PIXI.AnimatedSprite(clubsSS.animations.cards);
const card4 = new PIXI.AnimatedSprite(spadesSS.animations.cards);
const card5 = new PIXI.AnimatedSprite(diamondsSS.animations.cards);

const hand1 = new PIXI.AnimatedSprite(clubsSS.animations.cards);
const hand2 = new PIXI.AnimatedSprite(spadesSS.animations.cards);


hand1.y = 424;
hand2.y = 424;

hand1.x = 312;
hand2.x = 312 +88;



const cards = [card1, card2, card3, card4, card5]

cards.forEach((card)=>{
card.width *= 0.5;
card.height *= 0.5;
});

card2.currentFrame = 1;
card3.currentFrame = 2;
card4.currentFrame = 3;
card5.currentFrame = 4;


const baseBoardOffset = 275;

//handCard1.y = 400;


card1.x = baseBoardOffset;
card1.y = 250;

card2.y = 250;
card3.y = 250;
card4.y = 250;
card5.y = 250;

card2.x = baseBoardOffset + 50;
card3.x = baseBoardOffset + (50 *2);
card4.x = baseBoardOffset + (50 *3);
card5.x = baseBoardOffset + (50 *4);


app.stage.addChild(card1, card2, card3, card4, card5);

app.stage.addChild(hand1, hand2);


const gr  = new PIXI.Graphics();


playerLocations.forEach((playerLoc) => {

gr.beginFill(0xffffff);
gr.drawCircle(100+playerLoc.x, 100+playerLoc.y, 35);
gr.endFill();
app.stage.addChild(gr)

});
