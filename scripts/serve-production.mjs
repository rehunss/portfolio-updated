import http from 'node:http';
import {readFile,stat} from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {gzipSync} from 'node:zlib';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'../dist');
const base='/portfolio-preview/';
const types={'.html':'text/html; charset=utf-8','.js':'text/javascript','.css':'text/css','.svg':'image/svg+xml','.webp':'image/webp','.avif':'image/avif','.png':'image/png','.jpg':'image/jpeg','.jpeg':'image/jpeg','.pdf':'application/pdf','.woff2':'font/woff2','.woff':'font/woff','.json':'application/json'};
http.createServer(async(req,res)=>{
 try{const pathname=decodeURIComponent(new URL(req.url,'http://localhost').pathname);if(pathname==='/'){res.writeHead(302,{location:base});res.end();return;}if(!pathname.startsWith(base)){res.writeHead(404);res.end('Not found');return;}
 const relative=pathname.slice(base.length)||'index.html';const file=path.resolve(root,relative);if(file!==root&&!file.startsWith(root+path.sep)){res.writeHead(403);res.end();return;}
 if(!(await stat(file)).isFile()){res.writeHead(404);res.end();return;}let body=await readFile(file);const ext=path.extname(file);const compressed=/\b gzip\b|\bgzip\b/.test(req.headers['accept-encoding']||'')&&['.html','.js','.css','.svg','.json'].includes(ext);if(compressed)body=gzipSync(body);
 res.writeHead(200,{'Content-Type':types[ext]||'application/octet-stream','Content-Length':body.length,'Cache-Control':'no-cache','Vary':'Accept-Encoding',...(compressed?{'Content-Encoding':'gzip'}:{})});res.end(body);
 }catch{res.writeHead(404);res.end('Not found');}
}).listen(4173,'127.0.0.1',()=>console.log('Production preview: http://127.0.0.1:4173/portfolio-preview/'));
