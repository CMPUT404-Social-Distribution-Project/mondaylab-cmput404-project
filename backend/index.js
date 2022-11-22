import { join } from 'path'

// Serve static files from the React frontend app
app.use(express.static(join(__dirname, '../frontend/build')))

// AFTER defining routes: Anything that doesn't match what's above, send back index.html; (the beginning slash ('/') in the string is important!)
app.get('*', (req, res) => {
  res.sendFile(join(__dirname + '/../frontend/build/index.html'))
})