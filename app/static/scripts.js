async function plot(playlistName) {
  const url = `playlists/${playlistName}`;
  const data = await fetch(url).then((response) => response.json());

  Plotly.newPlot('release_years',
    [{x: data.release_years, type: 'histogram', xbins: {size: 1}}],
    {margin: { t: 0 } }
  );

  Plotly.newPlot('popularity',
    [{x: data.popularity, type: 'histogram', xbins: {size: 1}}],
    {margin: { t: 0 } }
  );
}

await plot('bestest');
