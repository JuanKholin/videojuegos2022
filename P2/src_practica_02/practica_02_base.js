/*
*
* Practica_02_base.js
* Videojuegos (30262) - Curso 2019-2020
*
* Parte adaptada de: Alex Clarke, 2016, y Ed Angel, 2015.
*
*/

// Variable to store the WebGL rendering context
var gl;

//----------------------------------------------------------------------------
// MODEL DATA
//----------------------------------------------------------------------------

//Define points' position vectors
const cubeVerts = [
	[ 0.5, 0.5, 0.5, 1], //0
	[ 0.5, 0.5,-0.5, 1], //1
	[ 0.5,-0.5, 0.5, 1], //2
	[ 0.5,-0.5,-0.5, 1], //3
	[-0.5, 0.5, 0.5, 1], //4
	[-0.5, 0.5,-0.5, 1], //5
	[-0.5,-0.5, 0.5, 1], //6
	[-0.5,-0.5,-0.5, 1], //7
];

const wireCubeIndices = [
//Wire Cube - use LINE_STRIP, starts at 0, 30 vertices
	0,4,6,2,0, //front
	1,0,2,3,1, //right
	5,1,3,7,5, //back
	4,5,7,6,4, //right
	4,0,1,5,4, //top
	6,7,3,2,6, //bottom
];

const cubeIndices = [
//Solid Cube - use TRIANGLES, starts at 0, 36 vertices
	0,4,6, //front
	0,6,2,
	1,0,2, //right
	1,2,3,
	5,1,3, //back
	5,3,7,
	4,5,7, //left
	4,7,6,
	4,0,1, //top
	4,1,5,
	6,7,3, //bottom
	6,3,2,
];

const pointsAxes = [];
pointsAxes.push([ 2.0, 0.0, 0.0, 1.0]); //x axis is green
pointsAxes.push([-2.0, 0.0, 0.0, 1.0]);
pointsAxes.push([ 0.0, 2.0, 0.0, 1.0]); //y axis is red
pointsAxes.push([ 0.0,-2.0, 0.0, 1.0]);
pointsAxes.push([ 0.0, 0.0, 2.0, 1.0]); //z axis is blue
pointsAxes.push([ 0.0, 0.0,-2.0, 1.0]);

const pointsWireCube = [];
for (let i=0; i < wireCubeIndices.length; i++)
{
	pointsWireCube.push(cubeVerts[wireCubeIndices[i]]);
}

const pointsCube = [];
for (let i=0; i < cubeIndices.length; i++)
{
	pointsCube.push(cubeVerts[cubeIndices[i]]);
}

const shapes = {
	wireCube: {Start: 0, Vertices: 30},
	cube: {Start: 0, Vertices: 36},
	axes: {Start: 0, Vertices: 6}
};

const red =			[1.0, 0.0, 0.0, 1.0];
const green =		[0.0, 1.0, 0.0, 1.0];
const blue =		[0.0, 0.0, 1.0, 1.0];
const lightred =	[1.0, 0.5, 0.5, 1.0];
const lightgreen =	[0.5, 1.0, 0.5, 1.0];
const lightblue = 	[0.5, 0.5, 1.0, 1.0];
const white =		[1.0, 1.0, 1.0, 1.0];

const colorsAxes = [
	green, green, //x
	red, red,     //y
	blue, blue,   //z
];

const colorsWireCube = [
	white, white, white, white, white,
	white, white, white, white, white,
	white, white, white, white, white,
	white, white, white, white, white,
	white, white, white, white, white,
	white, white, white, white, white,
];

// const colorsCube = [
// 	lightblue, lightblue, lightblue, lightblue, lightblue, lightblue,
// 	lightgreen, lightgreen, lightgreen, lightgreen, lightgreen, lightgreen,
// 	lightred, lightred, lightred, lightred, lightred, lightred,
// 	blue, blue, blue, blue, blue, blue,
// 	red, red, red, red, red, red,
// 	green, green, green, green, green, green,
// ];

const colorsCube = [
	white, white, white, white, white, white,
	white, white, white, white, white, white,
	white, white, white, white, white, white,
	white, white, white, white, white, white,
	white, white, white, white, white, white,
	white, white, white, white, white, white,
];

//----------------------------------------------------------------------------
// OTHER DATA
//----------------------------------------------------------------------------

var model = new mat4();   		// create a model matrix and set it to the identity matrix
var view = new mat4();   		// create a view matrix and set it to the identity matrix
var projection = new mat4();	// create a projection matrix and set it to the identity matrix

var eye, target, up;			// for view matrix

var rotAngle = 0.0;
var rotChange = 1;

var program;
var uLocations = {};
var aLocations = {};

var programInfo = {
			program,
			uniformLocations: {},
			attribLocations: {},
};

var objectsToDraw = [
		{
		  programInfo: programInfo,
		  pointsArray: pointsAxes,
		  colorsArray: colorsAxes,
		  uniforms: {
			u_colorMult: [1.0, 1.0, 1.0, 1.0],
			u_model: new mat4(),
		  },
		  primType: "lines",
		},
		{
		  programInfo: programInfo,
		  pointsArray: pointsWireCube,
		  colorsArray: colorsWireCube,
		  uniforms: {
			u_colorMult: [1.0, 1.0, 1.0, 1.0],
			u_model: new mat4(),
		  },
		  primType: "line_strip",
		},
		{
		  programInfo: programInfo,
		  pointsArray: pointsCube,
		  colorsArray: colorsCube,
		  uniforms: {
			u_colorMult: [1.0, 1.0, 1.0, 1.0],
			u_model: new mat4(),
		  },
		  primType: "triangles",
		  x: 0, y: 0, z: 0, rotChange: 0.5, rotAngle: 0.0,
			eje: new vec3(0.0, 1.0, 0.0),

		},
		{
		  programInfo: programInfo,
		  pointsArray: pointsCube,
		  colorsArray: colorsCube,
		  uniforms: {
			u_colorMult: [0.5, 0.5, 0.5, 1.0],
			u_model: new mat4(),
		  },
		  primType: "triangles",
		  x: 0, y: 0, z: 0, rotChange: 0.5, rotAngle: 0.0,
			eje: new vec3(0.0, 1.0, 0.0),

		},
		{
			programInfo: programInfo,
			pointsArray: pointsCube,
			colorsArray: colorsCube,
			uniforms: {
			  u_colorMult: [0.5, 0.5, 0.5, 1.0],
			  u_model: new mat4(),
			},
			primType: "triangles",
			x: 0, y: 0, z: 0, rotChange: 0.5, rotAngle: 0.0,
			eje: new vec3(0.0, 1.0, 0.0),

		  },
		  {
			programInfo: programInfo,
			pointsArray: pointsCube,
			colorsArray: colorsCube,
			uniforms: {
			  u_colorMult: [0.5, 0.5, 0.5, 1.0],
			  u_model: new mat4(),
			},
			primType: "triangles",
			x: 0, y: 0, z: 0, rotChange: 0.5, rotAngle: 0.0,
			eje: new vec3(0.0, 1.0, 0.0),

		  },
		  {
			programInfo: programInfo,
			pointsArray: pointsCube,
			colorsArray: colorsCube,
			uniforms: {
			  u_colorMult: [0.5, 0.5, 0.5, 1.0],
			  u_model: new mat4(),
			},
			primType: "triangles",
			x: 0, y: 0, z: 0, rotChange: 0.5, rotAngle: 0.0,
			eje: new vec3(0.0, 1.0, 0.0),

		  },
		  {
			programInfo: programInfo,
			pointsArray: pointsCube,
			colorsArray: colorsCube,
			uniforms: {
			  u_colorMult: [0.5, 0.5, 0.5, 1.0],
			  u_model: new mat4(),
			},
			primType: "triangles",
			x: 0, y: 0, z: 0, rotChange: 0.5, rotAngle: 0.0,
			eje: new vec3(0.0, 1.0, 0.0),

		  },
		  {
			programInfo: programInfo,
			pointsArray: pointsCube,
			colorsArray: colorsCube,
			uniforms: {
			  u_colorMult: [0.5, 0.5, 0.5, 1.0],
			  u_model: new mat4(),
			},
			primType: "triangles",
			x: 0, y: 0, z: 0, rotChange: 0.5, rotAngle: 0.0,
			eje: new vec3(0.0, 1.0, 0.0),

		  },
		  {
			programInfo: programInfo,
			pointsArray: pointsCube,
			colorsArray: colorsCube,
			uniforms: {
			  u_colorMult: [0.5, 0.5, 0.5, 1.0],
			  u_model: new mat4(),
			},
			primType: "triangles",
			x: 0, y: 0, z: 0, rotChange: 0.5, rotAngle: 0.0,
			eje: new vec3(0.0, 1.0, 0.0),

		  },
		  {
			programInfo: programInfo,
			pointsArray: pointsCube,
			colorsArray: colorsCube,
			uniforms: {
			  u_colorMult: [0.5, 0.5, 0.5, 1.0],
			  u_model: new mat4(),
			},
			primType: "triangles",
			x: 0, y: 0, z: 0, rotChange: 0.5, rotAngle: 0.0,
			eje: new vec3(0.0, 1.0, 0.0),

		  },
		  {
			programInfo: programInfo,
			pointsArray: pointsCube,
			colorsArray: colorsCube,
			uniforms: {
			  u_colorMult: [0.5, 0.5, 0.5, 1.0],
			  u_model: new mat4(),
			},
			primType: "triangles",
			x: 0, y: 0, z: 0, rotChange: 0.5, rotAngle: 0.0,
			eje: new vec3(0.0, 1.0, 0.0),

		  },
		  {
			programInfo: programInfo,
			pointsArray: pointsCube,
			colorsArray: colorsCube,
			uniforms: {
			  u_colorMult: [0.5, 0.5, 0.5, 1.0],
			  u_model: new mat4(),
			},
			primType: "triangles",
			x: 0, y: 0, z: 0, rotChange: 0.5, rotAngle: 0.0,
			eje: new vec3(0.0, 1.0, 0.0),

		  },
		  {
			programInfo: programInfo,
			pointsArray: pointsCube,
			colorsArray: colorsCube,
			uniforms: {
			  u_colorMult: [0.5, 0.5, 0.5, 1.0],
			  u_model: new mat4(),
			},
			primType: "triangles",
			x: 0, y: 0, z: 0, rotChange: 0.5, rotAngle: 0.0,
			eje: new vec3(0.0, 1.0, 0.0),

		  },
		  {
			programInfo: programInfo,
			pointsArray: pointsCube,
			colorsArray: colorsCube,
			uniforms: {
			  u_colorMult: [0.5, 0.5, 0.5, 1.0],
			  u_model: new mat4(),
			},
			primType: "triangles",
			x: 0, y: 0, z: 0, rotChange: 0.5, rotAngle: 0.0,
			eje: new vec3(0.0, 1.0, 0.0),

		  },
		  {
			programInfo: programInfo,
			pointsArray: pointsCube,
			colorsArray: colorsCube,
			uniforms: {
			  u_colorMult: [0.5, 0.5, 0.5, 1.0],
			  u_model: new mat4(),
			},
			primType: "triangles",
			x: 0, y: 0, z: 0, rotChange: 0.5, rotAngle: 0.0,
			eje: new vec3(0.0, 1.0, 0.0),

		  },
		  {
			programInfo: programInfo,
			pointsArray: pointsCube,
			colorsArray: colorsCube,
			uniforms: {
			  u_colorMult: [0.5, 0.5, 0.5, 1.0],
			  u_model: new mat4(),
			},
			primType: "triangles",
			x: 0, y: 0, z: 0, rotChange: 0.5, rotAngle: 0.0,
			eje: new vec3(0.0, 1.0, 0.0),

		  },
		  {
			programInfo: programInfo,
			pointsArray: pointsCube,
			colorsArray: colorsCube,
			uniforms: {
			  u_colorMult: [0.5, 0.5, 0.5, 1.0],
			  u_model: new mat4(),
			},
			primType: "triangles",
			x: 0, y: 0, z: 0, rotChange: 0.5, rotAngle: 0.0,
			eje: new vec3(0.0, 1.0, 0.0),

		  },
		  {
			programInfo: programInfo,
			pointsArray: pointsCube,
			colorsArray: colorsCube,
			uniforms: {
			  u_colorMult: [0.5, 0.5, 0.5, 1.0],
			  u_model: new mat4(),
			},
			primType: "triangles",
			x: 0, y: 0, z: 0, rotChange: 0.5, rotAngle: 0.0,
			eje: new vec3(0.0, 1.0, 0.0),

		  },
		  {
			programInfo: programInfo,
			pointsArray: pointsCube,
			colorsArray: colorsCube,
			uniforms: {
			  u_colorMult: [0.5, 0.5, 0.5, 1.0],
			  u_model: new mat4(),
			},
			primType: "triangles",
			x: 0, y: 0, z: 0, rotChange: 0.5, rotAngle: 0.0,
			eje: new vec3(0.0, 1.0, 0.0),

		  },
		  {
			programInfo: programInfo,
			pointsArray: pointsCube,
			colorsArray: colorsCube,
			uniforms: {
			  u_colorMult: [0.5, 0.5, 0.5, 1.0],
			  u_model: new mat4(),
			},
			primType: "triangles",
			x: 0, y: 0, z: 0, rotChange: 0.5, rotAngle: 0.0,
			eje: new vec3(0.0, 1.0, 0.0),

		  },
		  {
			programInfo: programInfo,
			pointsArray: pointsCube,
			colorsArray: colorsCube,
			uniforms: {
			  u_colorMult: [0.5, 0.5, 0.5, 1.0],
			  u_model: new mat4(),
			},
			primType: "triangles",
			x: 0, y: 0, z: 0, rotChange: 0.5, rotAngle: 0.0,
			eje: new vec3(0.0, 1.0, 0.0),
		  },


];

//----------------------------------------------------------------------------
// Initialization function
//----------------------------------------------------------------------------

window.onload = function init(){

	for(let i = 2; i < objectsToDraw.length; i++){
		let aux = Math.random()
		if(aux <= 0.33){
			objectsToDraw[i].z = Math.random() * (5 - 1) + 1;
			objectsToDraw[i].eje = vec3(Math.random() * 5, Math.random() * 5, 0.0)

		}
		else if(aux <= 0.66){
			objectsToDraw[i].x = Math.random() * (5 - 1) + 1;
			objectsToDraw[i].eje = vec3(0, Math.random()*5, Math.random()*5)
		}
		else {
			objectsToDraw[i].y = Math.random() * (5 - 1) + 1;
			objectsToDraw[i].eje = vec3(Math.random()*5, 0, Math.random()*5)
		}

		objectsToDraw[i].rotChange = Math.random() * (1 - 0.2) + 0.2;
		objectsToDraw[i].rotAngle = Math.random() * (3 - 0) + 0;
		objectsToDraw[i].uniforms.u_colorMult[0] = Math.random();
		objectsToDraw[i].uniforms.u_colorMult[1] = Math.random();
		objectsToDraw[i].uniforms.u_colorMult[2] = Math.random();
	}

	// Set up a WebGL Rendering Context in an HTML5 Canvas
	var canvas = document.getElementById("gl-canvas");
	gl = WebGLUtils.setupWebGL(canvas);
	if (!gl){
		alert("WebGL isn't available");
	}

	//  Configure WebGL
	gl.clearColor(0.0, 0.0, 0.0, 1.0);
	gl.enable(gl.DEPTH_TEST);

	setPrimitive(objectsToDraw);

	// Set up a WebGL program
	// Load shaders and initialize attribute buffers
	program = initShaders(gl, "vertex-shader", "fragment-shader");

	// Save the attribute and uniform locations
	uLocations.model = gl.getUniformLocation(program, "model");
	uLocations.view = gl.getUniformLocation(program, "view");
	uLocations.projection = gl.getUniformLocation(program, "projection");
	uLocations.colorMult = gl.getUniformLocation(program, "colorMult");
	aLocations.vPosition = gl.getAttribLocation(program, "vPosition");
	aLocations.vColor = gl.getAttribLocation(program, "vColor");

	programInfo.uniformLocations = uLocations;
	programInfo.attribLocations = aLocations;
	programInfo.program = program;

	gl.useProgram(programInfo.program);

	// Set up viewport
	gl.viewport(0, 0, gl.drawingBufferWidth, gl.drawingBufferHeight);

	// Set up camera
	// Projection matrix
	projection = perspective( 45.0, canvas.width/canvas.height, 0.1, 100.0 );
	gl.uniformMatrix4fv( programInfo.uniformLocations.projection, gl.FALSE, projection ); // copy projection to uniform value in shader
    // View matrix (static cam)
	eye = vec3(-5, 0, 0);
	target =  vec3(3.0, 0.0, 0.0);
	up =  vec3(0.0, 1.0, 0.0);
	view = lookAt(eye,target,up);
	gl.uniformMatrix4fv(programInfo.uniformLocations.view, gl.FALSE, view); // copy view to uniform value in shader

	// Para ajustar la velocidad de la cámara, ojalá tan fácil en la realidad
	let camSpeed = 0.1;
	let isOrtoPersp = false;
	let scale = 4;
	let fov = 45;
	// Define los eventos de pulsar tecla
	window.addEventListener("keydown", function(event){
		if (event.defaultPrevented){
			return; // No se hace nada si se ha hecho ya
		}
		// Vector dirección desde donde se mira hacia donde se mira (eye->target)
		let aux = vec3(0, 0, 0);
		aux[0] = target[0] - eye[0];
		aux[1] = target[1] - eye[1];
		aux[2] = target[2] - eye[2];
		// Lo unitarizamos, sé que suena mal pero no se me ocurre otro término
		let mod = math.sqrt(aux[0] * aux[0] + aux[1] * aux[1] + aux[2] * aux[2]);
		aux[0] = aux[0] / mod;
		aux[1] = aux[1] / mod;
		aux[2] = aux[2] / mod;
		let vectY = vec3(0, 1, 0);
		let perp = vec3(0, 0, 0);
		switch(event.code){
		case "ArrowDown":
			if (isOrtoPersp == true){
				scale = scale * 1.01;
				if (scale > 30){
					scale = 30;
				}
				projection = ortho(scale * -canvas.width / canvas.height,
						scale * canvas.width / canvas.height, -scale, scale, 0.1, 100);
				gl.uniformMatrix4fv( programInfo.uniformLocations.projection, gl.FALSE, projection );
			}else{
				eye[0] = eye[0] - camSpeed * aux[0];
				target[0] = target[0] - camSpeed * aux[0];
				eye[1] = eye[1] - camSpeed * aux[1];
				target[1] = target[1] - camSpeed * aux[1];
				eye[2] = eye[2] - camSpeed * aux[2];
				target[2] = target[2] - camSpeed * aux[2];
				view = lookAt(eye, target, up);
				gl.uniformMatrix4fv(programInfo.uniformLocations.view, gl.FALSE, view);
			}
			break;
		case "ArrowUp":
			if (isOrtoPersp == true){
				scale = scale * 0.99;
				if (scale < 1){
					scale = 1;
				}
				projection = ortho(scale * -canvas.width / canvas.height,
						scale * canvas.width / canvas.height, -scale, scale, 0.1, 100);
				gl.uniformMatrix4fv( programInfo.uniformLocations.projection, gl.FALSE, projection );
			}else{
				eye[0] = eye[0] + camSpeed * aux[0];
				target[0] = target[0] + camSpeed * aux[0];
				eye[1] = eye[1] + camSpeed * aux[1];
				target[1] = target[1] + camSpeed * aux[1];
				eye[2] = eye[2] + camSpeed * aux[2];
				target[2] = target[2] + camSpeed * aux[2];
				view = lookAt(eye, target, up);
				gl.uniformMatrix4fv(programInfo.uniformLocations.view, gl.FALSE, view);
			}
			break;
		case "ArrowLeft":
			perp[0] = vectY[1] * aux[2] - vectY[2] * aux[1];
			perp[1] = vectY[0] * aux[2] - vectY[2] * aux[0];
			perp[2] = vectY[0] * aux[1] - vectY[1] * aux[0];
			eye[0] = eye[0] + camSpeed * perp[0];
			eye[1] = eye[1] + camSpeed * perp[1];
			eye[2] = eye[2] + camSpeed * perp[2];
			target[0] = target[0] + camSpeed * perp[0];
			target[1] = target[1] + camSpeed * perp[1];
			target[2] = target[2] + camSpeed * perp[2];
			view = lookAt(eye, target, up);
			gl.uniformMatrix4fv(programInfo.uniformLocations.view, gl.FALSE, view);
			break;
		case "ArrowRight":
			perp[0] = vectY[1] * aux[2] - vectY[2] * aux[1];
			perp[1] = vectY[0] * aux[2] - vectY[2] * aux[0];
			perp[2] = vectY[0] * aux[1] - vectY[1] * aux[0];
			eye[0] = eye[0] - camSpeed * perp[0];
			eye[1] = eye[1] - camSpeed * perp[1];
			eye[2] = eye[2] - camSpeed * perp[2];
			target[0] = target[0] - camSpeed * perp[0];
			target[1] = target[1] - camSpeed * perp[1];
			target[2] = target[2] - camSpeed * perp[2];
			view = lookAt(eye, target, up);
			gl.uniformMatrix4fv(programInfo.uniformLocations.view, gl.FALSE, view);
			break;
		case "KeyP":
			isOrtoPersp = false;
			projection = perspective( fov, canvas.width / canvas.height, 0.1, 100.0 );
			gl.uniformMatrix4fv( programInfo.uniformLocations.projection, gl.FALSE, projection );
			break;
		case "KeyO":
			isOrtoPersp = true;
			scale = 4;
			projection = ortho(scale * -canvas.width / canvas.height,
					scale * canvas.width / canvas.height, -scale, scale, 0.1, 100);
			gl.uniformMatrix4fv( programInfo.uniformLocations.projection, gl.FALSE, projection );
			break;
		case "BracketRight":
		case "NumpadAdd":
			if (isOrtoPersp == false){
				fov += 1;
				if (fov > 170){
					fov = 170;
				}
				projection = perspective( fov, canvas.width / canvas.height, 0.1, 100.0 );
				gl.uniformMatrix4fv( programInfo.uniformLocations.projection, gl.FALSE, projection );
			}
			break;
		case "Slash":
		case "NumpadSubtract":
			if (isOrtoPersp == false){
				fov -= 1;
				if (fov < 1){
					fov = 1;
				}
				projection = perspective( fov, canvas.width / canvas.height, 0.1, 100.0 );
				gl.uniformMatrix4fv( programInfo.uniformLocations.projection, gl.FALSE, projection );
			}
			break;
		}
		event.preventDefault();
	}, true);

	// Parte ratón
	let isClicked = false;
	let alfa = 0;
	let beta = 0;
	let x, y;

	window.addEventListener("mousedown", e =>{
		if (isClicked == false){
			isClicked = true
			x = e.clientX;
			y = e.clientY;
		}
	});

	window.addEventListener("mouseup", e=>{
		if (isClicked){
			isClicked = false;
		}
	});

	window.addEventListener("mousemove", e=>{
		let betaOffset = 0;
		let betaAux = 0;
		if (isClicked){
			if (e.clientX != x){ // Rotar horizontalmente
				alfa = alfa + (e.clientX - x);
				x = e.clientX;
				alfa = (alfa + 360) % 360; // Para corregir desbordamientos
			}
			if (e.clientY != y){
				betaAux = beta - (e.clientY - y);
				y = e.clientY;
				if (betaAux > 90){
					beta = 89.9;
				}else if (betaAux < -90){
					beta = -89.9;
				}else{
					beta = betaAux;
				}
			}
			let alfaRad = alfa * Math.PI / 180;
			let betaRad = beta * Math.PI / 180;
			target[0] = Math.cos(betaRad) * Math.cos(alfaRad) + eye[0];
			target[1] = Math.sin(betaRad) + eye[1];
			target[2] = Math.cos(betaRad) * Math.sin(alfaRad) + eye[2];
			view = lookAt(eye, target, up);
			gl.uniformMatrix4fv(programInfo.uniformLocations.view, gl.FALSE, view);
		}
	});


	requestAnimFrame(render);

};

//----------------------------------------------------------------------------
// Rendering Event Function
//----------------------------------------------------------------------------

function render() {

	gl.clear(gl.DEPTH_BUFFER_BIT | gl.COLOR_BUFFER_BIT);

	//----------------------------------------------------------------------------
	// MOVE STUFF AROUND
	//----------------------------------------------------------------------------

	let ejeY = vec3(0.0, 1.0, 0.0);
	let ejeX = vec3(1.0, 0.0, 0.0);

	for(let i = 2; i < objectsToDraw.length; i++){
		let Ry = rotate(objectsToDraw[i].rotAngle, objectsToDraw[i].eje);
		let Rx = rotate(objectsToDraw[i].rotAngle, ejeX);
		objectsToDraw[i].uniforms.u_model = translate(objectsToDraw[i].x, objectsToDraw[i].y, objectsToDraw[i].z);
		objectsToDraw[i].uniforms.u_model = mult(Ry, objectsToDraw[i].uniforms.u_model);
		//objectsToDraw[i].uniforms.u_model = mult(Rx, objectsToDraw[i].uniforms.u_model);
		objectsToDraw[i].uniforms.u_model = mult(objectsToDraw[i].uniforms.u_model, Ry);
		//objectsToDraw[i].uniforms.u_model = mult(objectsToDraw[i].uniforms.u_model, Rx);

	}

	let R = rotate(rotAngle, ejeY);

	//----------------------------------------------------------------------------
	// DRAW
	//----------------------------------------------------------------------------

	objectsToDraw.forEach(function(object) {

		gl.useProgram(object.programInfo.program);

		// Setup buffers and attributes
		setBuffersAndAttributes(object.programInfo, object.pointsArray, object.colorsArray);

		// Set the uniforms
		setUniforms(object.programInfo, object.uniforms);

		// Draw
		gl.drawArrays(object.primitive, 0, object.pointsArray.length);
    });

	for(let i = 2; i < objectsToDraw.length; i++){
		objectsToDraw[i].rotAngle += objectsToDraw[i].rotChange;
	}

	rotAngle += rotChange;

	requestAnimationFrame(render);

}

//----------------------------------------------------------------------------
// Utils functions
//----------------------------------------------------------------------------

function setPrimitive(objectsToDraw) {

	objectsToDraw.forEach(function(object) {
		switch(object.primType) {
		  case "lines":
			object.primitive = gl.LINES;
			break;
		  case "line_strip":
			object.primitive = gl.LINE_STRIP;
			break;
		  case "triangles":
		    object.primitive = gl.TRIANGLES;
		    break;
		  default:
			object.primitive = gl.TRIANGLES;
		}
	});
}

function setUniforms(pInfo, uniforms) {
	// Copy uniform model values to corresponding values in shaders
	gl.uniform4f(pInfo.uniformLocations.colorMult, uniforms.u_colorMult[0], uniforms.u_colorMult[1], uniforms.u_colorMult[2], uniforms.u_colorMult[3]);
	gl.uniformMatrix4fv(pInfo.uniformLocations.model, gl.FALSE, uniforms.u_model);
}

function setBuffersAndAttributes(pInfo, ptsArray, colArray) {
	// Load the data into GPU data buffers
	// Vertices
	var vertexBuffer = gl.createBuffer();
	gl.bindBuffer( gl.ARRAY_BUFFER, vertexBuffer );
	gl.bufferData( gl.ARRAY_BUFFER,  flatten(ptsArray), gl.STATIC_DRAW );
	gl.vertexAttribPointer( pInfo.attribLocations.vPosition, 4, gl.FLOAT, gl.FALSE, 0, 0 );
	gl.enableVertexAttribArray( pInfo.attribLocations.vPosition );

	// Colors
	var colorBuffer = gl.createBuffer();
	gl.bindBuffer( gl.ARRAY_BUFFER, colorBuffer );
	gl.bufferData( gl.ARRAY_BUFFER,  flatten(colArray), gl.STATIC_DRAW );
	gl.vertexAttribPointer( pInfo.attribLocations.vColor, 4, gl.FLOAT, gl.FALSE, 0, 0 );
	gl.enableVertexAttribArray( pInfo.attribLocations.vColor );
}
