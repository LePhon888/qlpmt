 function SomeDeleteRowFunction(o, benhnhan) {
     let p=o.parentNode.parentNode;
     let answer = confirm(`${'Bạn có chắn chắn xóa bệnh nhân '}${benhnhan}`);
     if (answer) {
        p.parentNode.removeChild(p);
     }
}