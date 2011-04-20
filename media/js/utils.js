function format(){
 
    var formatted_str = arguments[0] || '';
 
    for(var i=1; i<arguments.length; i++){
        var re = new RegExp("\\{"+(i-1)+"}", "gim");
        formatted_str = formatted_str.replace(re, arguments[i]);
    }
    
    return formatted_str;
};

function dict_format(){
    var formatted_str = arguments[0] || '';
    var dict = arguments[1];
    for(var key in dict){
        var re = new RegExp("\\{"+key+"}", "gim");
        formatted_str = formatted_str.replace(re, dict[key]);
    }
    return formatted_str;
}

function toggleFieldHelp(event, item, hide){
    var val = item.value.trim();
    var help = item.getSiblings(format('span.help_text[rel={0}]', item.name))[0];
    
    if (hide === true ){
        return help.hide(); 
    } else if (val === ''){
        return (help.hasClass('inline'))? help.setStyle('display', 'inline'): help.show(); 
    } 
    return help.hide(); 
};

/**
*
*  UTF-8 data encode / decode
*  http://www.webtoolkit.info/
*
**/
 
var Utf8 = {
 
	// public method for url encoding
	encode : function (string) {
		string = string.replace(/\r\n/g,"\n");
		var utftext = "";
 
		for (var n = 0; n < string.length; n++) {
 
			var c = string.charCodeAt(n);
 
			if (c < 128) {
				utftext += String.fromCharCode(c);
			}
			else if((c > 127) && (c < 2048)) {
				utftext += String.fromCharCode((c >> 6) | 192);
				utftext += String.fromCharCode((c & 63) | 128);
			}
			else {
				utftext += String.fromCharCode((c >> 12) | 224);
				utftext += String.fromCharCode(((c >> 6) & 63) | 128);
				utftext += String.fromCharCode((c & 63) | 128);
			}
 
		}
 
		return utftext;
	},
 
	// public method for url decoding
	decode : function (utftext) {
		var string = "";
		var i = 0;
		var c = c1 = c2 = 0;
 
		while ( i < utftext.length ) {
 
			c = utftext.charCodeAt(i);
 
			if (c < 128) {
				string += String.fromCharCode(c);
				i++;
			}
			else if((c > 191) && (c < 224)) {
				c2 = utftext.charCodeAt(i+1);
				string += String.fromCharCode(((c & 31) << 6) | (c2 & 63));
				i += 2;
			}
			else {
				c2 = utftext.charCodeAt(i+1);
				c3 = utftext.charCodeAt(i+2);
				string += String.fromCharCode(((c & 15) << 12) | ((c2 & 63) << 6) | (c3 & 63));
				i += 3;
			}
 
		}
 
		return string;
	}
 
}

