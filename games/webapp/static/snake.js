(() => {
  const canvas = document.getElementById('c')
  const ctx = canvas.getContext('2d')
  const grid = 20
  const cols = canvas.width / grid
  const rows = canvas.height / grid

  let snake = [{x: Math.floor(cols/2), y: Math.floor(rows/2)}]
  let dir = {x:1,y:0}
  let food = null
  let score = 0
  let running = false
  let interval = null

  // audio setup
  const AudioCtx = window.AudioContext || window.webkitAudioContext
  const aCtx = AudioCtx ? new AudioCtx() : null
  function playSound(kind){
    if(!aCtx) return
    const o = aCtx.createOscillator()
    const g = aCtx.createGain()
    o.connect(g); g.connect(aCtx.destination)
    if(kind==='eat'){ o.frequency.value = 880; g.gain.value = 0.06 }
    else if(kind==='crash'){ o.frequency.value = 120; g.gain.value = 0.12 }
    else if(kind==='move'){ o.frequency.value = 440; g.gain.value = 0.03 }
    o.type = 'sine'
    o.start()
    g.gain.exponentialRampToValueAtTime(0.0001, aCtx.currentTime + 0.12)
    setTimeout(()=>o.stop(),140)
  }

  function placeFood(){
    let ok=false
    while(!ok){
      const x = Math.floor(Math.random()*cols)
      const y = Math.floor(Math.random()*rows)
      ok = !snake.some(s=>s.x===x && s.y===y)
      if(ok) food = {x,y}
    }
  }

  function reset(){
    snake = [{x: Math.floor(cols/2), y: Math.floor(rows/2)}]
    dir = {x:1,y:0}
    score = 0
    document.getElementById('score').textContent = score
    placeFood()
    draw()
  }

  function tick(){
    const head = {x: snake[0].x + dir.x, y: snake[0].y + dir.y}
    // walls
    if(head.x < 0 || head.x >= cols || head.y < 0 || head.y >= rows){
      gameOver(); return
    }
    // self collision
    if(snake.some(s=>s.x===head.x && s.y===head.y)) { gameOver(); return }
    snake.unshift(head)
    // food
    if(food && head.x===food.x && head.y===food.y){
      score += 1
      document.getElementById('score').textContent = score
      placeFood()
      playSound('eat')
    } else {
      snake.pop()
    }
    draw()
  }

  function draw(){
    ctx.clearRect(0,0,canvas.width,canvas.height)
    // background grid subtle
    ctx.fillStyle = '#071026'
    ctx.fillRect(0,0,canvas.width,canvas.height)
    // food
    if(food){
      ctx.fillStyle = '#ff595e'
      ctx.fillRect(food.x*grid+2, food.y*grid+2, grid-4, grid-4)
    }
    // snake
    ctx.fillStyle = '#8bd3dd'
    snake.forEach((s,i)=>{
      ctx.fillStyle = i===0 ? '#6be3b6' : '#8bd3dd'
      ctx.fillRect(s.x*grid+1, s.y*grid+1, grid-2, grid-2)
    })
  }

  function gameOver(){
    running = false
    clearInterval(interval)
    playSound('crash')
    setTimeout(async ()=>{
      try{
        const nameEl = document.getElementById('playerName')
        const name = (nameEl && nameEl.value) ? nameEl.value : prompt('Game over! Enter your name for the leaderboard:', 'Player')
        if(name){
          await fetch('/api/score', {method:'POST', headers:{'content-type':'application/json'}, body: JSON.stringify({name, score})})
        }
      }catch(e){/* ignore */}
      alert('Game over — score: '+score)
    }, 80)
  }

  document.addEventListener('keydown', e=>{
    const k = e.key
    if(k==='ArrowUp' || k==='w') { if(dir.y!==1) dir={x:0,y:-1} }
    if(k==='ArrowDown' || k==='s') { if(dir.y!==-1) dir={x:0,y:1} }
    if(k==='ArrowLeft' || k==='a') { if(dir.x!==1) dir={x:-1,y:0} }
    if(k==='ArrowRight' || k==='d') { if(dir.x!==-1) dir={x:1,y:0} }
  })

  // touch controls
  function touchDir(d){ if(d==='up' && dir.y!==1) dir={x:0,y:-1}; if(d==='down' && dir.y!==-1) dir={x:0,y:1}; if(d==='left' && dir.x!==1) dir={x:-1,y:0}; if(d==='right' && dir.x!==-1) dir={x:1,y:0} }
  ['up','left','down','right'].forEach(n=>{
    const el = document.getElementById('tc-'+n)
    if(el){
      el.addEventListener('touchstart', e=>{ e.preventDefault(); touchDir(n); playSound('move') })
      el.addEventListener('mousedown', e=>{ e.preventDefault(); touchDir(n) })
    }
  })

  document.getElementById('start').addEventListener('click', ()=>{
    if(running) return
    running = true
    if(!food) placeFood()
    interval = setInterval(tick, 120)
  })
  document.getElementById('pause').addEventListener('click', ()=>{
    if(!running) return
    running = false
    clearInterval(interval)
  })
  document.getElementById('reset').addEventListener('click', ()=>{
    clearInterval(interval)
    running=false
    reset()
  })

  // init
  reset()
})()
