<template>
  <div id="app">
    <div>
      <b-navbar toggleable="lg" type="dark" variant="dark">
        <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>

        <b-collapse id="nav-collapse" is-nav right>
          <b-navbar-nav>
            <b-navbar-brand href="/" id="link" class="btn btn-dark">Home</b-navbar-brand>
            <b-navbar-brand href="/about" id="link" class="btn btn-dark">About</b-navbar-brand>
          </b-navbar-nav>
        </b-collapse>
      </b-navbar>
    </div>

    <router-view/>
  </div>
</template>


<style>
body {
  background-image: url(./assets/background.jpg);
  background-repeat: no-repeat;
  background-size: cover;
}

#app {
  font-family: "Avenir", Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

#link {
  font-weight: bold;
  font-family: Helvetica;
}
</style>
