/* Make a real calendar file for each dated event: cal/<id>.ics, served by the site.
   iPhones and Macs open a real .ics link straight into "Add to calendar" (a generated blob often does nothing).
   Run after changing EVENTS in hello.html: node tools/build_cal.js */
const fs=require('fs'), path=require('path'), vm=require('vm');
const root=path.join(__dirname,'..'), html=fs.readFileSync(path.join(root,'hello.html'),'utf8');
const m=html.match(/var EVENTS = (\[[\s\S]*?\n\]);/); if(!m) throw new Error('EVENTS not found');
const EVENTS=vm.runInNewContext('('+m[1]+')');
const SITE='https://vavavoom.town/hello.html';
function utc(local){ // local Europe/London 'YYYY-MM-DDTHH:MM' -> UTC 'YYYYMMDDTHHMMSSZ'
  const guess=new Date(local+':00Z');
  const lon=new Date(guess.toLocaleString('en-US',{timeZone:'Europe/London'}));
  const off=lon-new Date(guess.toLocaleString('en-US',{timeZone:'UTC'}));
  return new Date(guess-off).toISOString().replace(/[-:]/g,'').split('.')[0]+'Z';
}
function esc(s){ return String(s).replace(/\\/g,'\\\\').replace(/;/g,'\;').replace(/,/g,'\\,').replace(/\n/g,'\\n'); }
fs.mkdirSync(path.join(root,'cal'),{recursive:true});
let n=0;
for(const ev of EVENTS){ if(!ev.start||!ev.end) continue;
  const ics=['BEGIN:VCALENDAR','VERSION:2.0','PRODID:-//Va Va Voom//Godalming//EN','CALSCALE:GREGORIAN','METHOD:PUBLISH','BEGIN:VEVENT',
    'UID:'+ev.id+'-'+ev.start.replace(/\D/g,'')+'@vavavoom.town','DTSTAMP:'+new Date().toISOString().replace(/[-:]/g,'').split('.')[0]+'Z',
    'DTSTART:'+utc(ev.start),'DTEND:'+utc(ev.end),'SUMMARY:'+esc(/va va voom/i.test(ev.title)?ev.title:ev.title+' (Va Va Voom)'),'LOCATION:'+esc(ev.where),
    'DESCRIPTION:'+esc('With '+ev.host+'. Details: '+SITE+'#'+ev.id),'URL:'+SITE+'#'+ev.id,'END:VEVENT','END:VCALENDAR'].join('\r\n')+'\r\n';
  fs.writeFileSync(path.join(root,'cal',ev.id+'.ics'),ics); n++; }
console.log(n+' calendar files written');
