$input a_position, a_color0//, a_texcoord0
$output v_position,v_color0,v_normal//, v_texcoord0

#include <bgfx_shader.sh>
#include "packing.comp"
uniform vec4 _offset;

void main()
{
	
	ivec3 pos = float_to_vec3_uint8(a_position.x);
	ivec3 normal = float_to_vec3_uint8(a_position.y)-ivec3(1,1,1);
	pos = pos + _offset;
	//vec3 pos = texture2d(s_texture_lookup,vec2(0,0));
	gl_Position = mul(u_modelViewProj, vec4(pos, 1.0) );
	//float test = color2float(vec3(a_color0,0,0));

	vec3 color = float_to_vec3(a_color0,256);
	v_position = pos;
	//pos = vec3(255,255,255);
	v_color0 = vec4(color,1);
	v_normal = normal;
	//v_normal = a_normal;
}