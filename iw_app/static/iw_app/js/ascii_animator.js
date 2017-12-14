// http://www.w3schools.com/howto/howto_js_animate.asp
// http://www.w3schools.com/howto/tryit.asp?filename=tryhow_js_animate_3
// http://www.w3schools.com/jsref/met_win_setinterval.asp

var initial_elem = $('#logo').find('span')
var matrix = []
var m_xpos = 0;
var m_ypos = 0;
var current_frame = 0;
var frame_1 = JSON.parse(frames);
var frame_number = frame_1.length -1;

function createMatrix(input_array, column_count){
  var temp_array = []
  var index = 1
  for (i = 0; i < input_array.length; i++) {
    if (index == column_count) {
      //console.log(index)
      index = 1
      temp_array.push(input_array[i])
      //console.log(temp_array)
      matrix.push(temp_array)
      temp_array = []
    }
    else {
      //console.log(index)
      index ++
      temp_array.push(input_array[i])
      //console.log(temp_array)
    }
  }
}

/* JSON to frame transforms a JSON element into  */
function jsonToFrame(frame, matrix, f_num){
  var width = matrix[0].length;
  var height = matrix.length;
  var color = "";

  for (i = 0; i < height; i ++){
    for (j = 0; j < width; j ++){
      color = "rgba"+frame[f_num][i][j];
      matrix[i][j].style.color = color;
    }
  }
  //console.log(color);
}


function render_frame(){
  jsonToFrame(frame_1, matrix, current_frame);
  //console.log(current_frame)
  if (current_frame < frame_number){
    current_frame += 1;
  } else {
    current_frame = 0;
  }
}

//jsonToFrame(indv_frame, matrix);
createMatrix(initial_elem, 82);//82 for your INTERFASU thing
var id = setInterval(render_frame, 100);


//console.log(matrix);
// NOTE arrays are 0 indexed in js
//console.log(matrix[0][0]);
//console.log(matrix[2][2]);
//console.log(frame_1[1][1]);
