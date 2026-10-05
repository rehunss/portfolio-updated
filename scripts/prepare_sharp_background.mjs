import {createRequire} from 'node:module';
import {copyFile,writeFile,readFile} from 'node:fs/promises';
import {createHash} from 'node:crypto';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
const require=createRequire(import.meta.url);
const sharp=require('C:/Users/Hp/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/sharp');
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const input=process.argv[2];
if(!input)throw new Error('Pass the image-tool output path.');
const native=path.join(root,'artwork/continuous-world-sharp-native.png');
await copyFile(input,native);
const meta=await sharp(native).metadata();
const width=meta.width*4,height=meta.height*4;
await sharp(native).resize(width,height,{kernel:'nearest'}).png({compressionLevel:9}).toFile(path.join(root,'artwork/continuous-world-sharp-4x.png'));
const file='assets/continuous-world-sharp-4x.webp';
const output=path.join(root,'public',file);
await sharp(native).resize(width,height,{kernel:'nearest'}).webp({lossless:true,effort:6}).toFile(output);
const bytes=await readFile(output);
for(const factor of [2,4]){
 await sharp(native).resize(meta.width*factor,meta.height*factor,{kernel:'nearest'}).avif({quality:80,chromaSubsampling:'4:4:4',effort:5}).toFile(path.join(root,`public/assets/continuous-world-sharp-${factor}x.avif`));
}
const manifest=JSON.parse(await readFile(path.join(root,'asset-manifest.json'),'utf8'));
const entry={file,type:'generated-decoration',original:'artwork/continuous-world-sharp-native.png',master:'artwork/continuous-world-sharp-4x.png',evidence:false,purpose:'Sharper uninterrupted town-to-core pixel background',nativeDimensions:[meta.width,meta.height],dimensions:[width,height],transform:'4x nearest-neighbor pixel-preserving export and lossless WebP encoding; no claim of additional native detail',sha256:createHash('sha256').update(bytes).digest('hex'),prompts:'artwork/continuous-world-sharp-prompt.json'};
const index=manifest.findIndex(x=>x.file===file);if(index<0)manifest.push(entry);else manifest[index]=entry;
for(const factor of [2,4]){
 const avifFile=`assets/continuous-world-sharp-${factor}x.avif`;
 const data=await readFile(path.join(root,'public',avifFile));
 const avifEntry={...entry,file:avifFile,dimensions:[meta.width*factor,meta.height*factor],transform:`${factor}x nearest-neighbor pixel-preserving export, AVIF quality 80 with full 4:4:4 color; no claim of additional native detail`,sha256:createHash('sha256').update(data).digest('hex')};
 const existing=manifest.findIndex(x=>x.file===avifFile);if(existing<0)manifest.push(avifEntry);else manifest[existing]=avifEntry;
}
await writeFile(path.join(root,'asset-manifest.json'),JSON.stringify(manifest,null,2)+'\n','utf8');
console.log(JSON.stringify({native:entry.nativeDimensions,export:entry.dimensions,bytes:bytes.length,file}));
