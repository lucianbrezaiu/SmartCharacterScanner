<template>
  <div class="home">
    <!-- <HelloWorld msg="Welcome to Your Vue.js App"/> -->

    <div id="empty"></div>
    <template>
      <div>
        <b-form-file id="input" ref="input" class="mb-2" @change="updateCanvasImage" value accept=".jpg, .jpeg, .png"></b-form-file>

      </div>
    </template>

    <div id="bigContainer">

      <div id="leftContainer">
        <canvas ref="imageCanvas"></canvas>
      </div>

      <textarea id="rightContainer" wrap="off"></textarea> 

    </div>

    <b-progress id="bar" ref="bar" :value="val" variant="success" aria-valuemin="0" aria-valuemax="100"></b-progress>

    <button id="bt" ref="convertButton" type="button" class="btn btn-primary" v-on:click="convertImage" disabled="true">CONVERT</button>
    <button id="bt" ref="resetButton" type="button" class="btn btn-primary" v-on:click="reset" disabled="true">RESET</button>
    <button id="bt" ref="exportButton" type="button" class="btn btn-primary" v-on:click="exportText" disabled="true">EXPORT</button>

  </div>
</template>

<script>
import axios from "axios";
import jsPDF from 'jspdf';
import Base64 from 'js-base64';
// @ is an alias to /src
// import HelloWorld from "@/components/HelloWorld.vue";

export default {
  name: "home",

  data() {
    return {
        val: 0,
    }
      
  },

  methods: {
    updateCanvasImage(e) {
      this.val = 100
      var reader,
        files = e.target.files;

      var reader = new FileReader();
      var canvas = this.$refs.imageCanvas;

      this.$refs.convertButton.disabled = false

      reader.readAsDataURL(files[0]);
      reader.onload = function(e) {

        var img = new Image();
        img.src = e.target.result;

        img.onload = function(e) {
          canvas.width = img.width;
          canvas.height = img.height;

          var ctx = canvas.getContext("2d");
          ctx.drawImage(img, 0, 0);
          document.getElementById('rightContainer').value = ""
        };
      };
    },

    reset(e){
      this.val = 0
      this.$refs.resetButton.disabled = true
      this.$refs.exportButton.disabled = true
      this.$refs.input.reset()
      var canvas =  this.$refs.imageCanvas
      var ctx = canvas.getContext("2d")
      ctx.clearRect(0, 0, canvas.width, canvas.height)

      document.getElementById('rightContainer').value = ""

    },

    getIcon()
    {
      return "data:image/jpeg;base64," + new Buffer('./assets/vue.jpeg').toString('base64')
    },

    exportText(e)
    {
      const doc = new jsPDF("p","mm","a4")

      doc.setFont('times');

      doc.text(15,20,doc.splitTextToSize( document.getElementById('rightContainer').value,180))

      doc.save('ocr.pdf')
      
    },

    convertImage(e) {
      this.$refs.bar.animated = true
      this.$refs.convertButton.disabled = true; 
      var canvas = this.$refs.imageCanvas;
      var context = canvas.getContext("2d");
      
      var request = {
        width: canvas.width,
        height: canvas.height,
        data: Array.from(context.getImageData(0, 0, canvas.width, canvas.height).data)
      };

      axios
        .post("http://localhost:3000/recognize", request)
        .then(response => {
          this.$refs.bar.animated = false
          document.getElementById('rightContainer').value = response.data
          this.$refs.resetButton.disabled = false
          this.$refs.exportButton.disabled = false
          // alert("Operation completed!");
        })
        .catch(error => {
          alert("Server error!");
        });
      this.val = 100
    },

    rotateImage(e){
      var canvas = this.$refs.imageCanvas;
      var context = canvas.getContext("2d");

      imgwidth = canvas.width;
      imgheight = canvas.height;
      context.save();
      context.translate(imgwidth/2, imgheight/2);
      context.rotate(Math.PI/2);
      context.drawImage(sourceimage, -(imgwidth/2), -(imgheight/2));
      context.restore();
    }
  }
};
</script>

<style scoped>
h1 {
  color: black;
}

#bigContainer {
  display: flex;
  flex-direction: row;
  /* border: 10px solid black; */
  height: 500px;
}

#leftContainer {
  background-color: white;
  height: auto;
  width: 45%;
  position: relative;
  border-style: solid;
  border-radius: 9px;
  border-width: 5px;
  border-color: black;
  margin: 2%;
}

canvas {
  background-color: white;
  margin: auto;
  position: absolute;
  top: 50%;
  left: 50%;
  -ms-transform: translate(-50%, -50%);
  transform: translate(-50%, -50%);
  max-height: 100%;
  max-width: 100%;
}

#rightContainer {
  background-color: white;
  height: auto;
  width: 45%;
  position: relative;
  border-style: inset;
  border-width: 5px;
  border-color: black;
  margin: 2%;
  resize: none;
  overflow-y: auto;
  overflow-x: auto;
}

#bt {
  position: relative;
  margin: 2%;
  /* display: inline; */
  width: 400px;

}

#input{
  background-color: white;
  height: 40px;
 
}

#inputContainer{
  background-color: white;
  height: auto;
  width:100%;
  /* margin: 2%; */
  border-radius: 5px;
  border-width: 1px;
  border-color: black;
  border-style: solid;
  margin-left:3%;
  margin-right:3%;
}

#empty{
  height: 50px;
}

#bar{
  margin-left:3%;
  margin-right:3%;
  height:40px;
}

</style>