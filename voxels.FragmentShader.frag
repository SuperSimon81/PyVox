$input v_position,v_color0,v_normal //,v_texcoord0

#include <bgfx_shader.sh>
uniform vec4 _eye_pos;
uniform vec4 _fog_color;
uniform vec4 _light;
float getFogFactor(float d)
{
    const float FogMax = 150.0;
    const float FogMin = 90.0;

    if (d>=FogMax) return 1;
    if (d<=FogMin) return 0;

    return 1 - (FogMax - d) / (FogMax - FogMin);
}

void main()
{

	//vec4 V = v_position;
    float d = distance(_eye_pos, v_position);
    float alpha = getFogFactor(d);


    vec3 norm = normalize(vec3(v_normal));
    vec3 lightDir = normalize(_light - v_position);  

    float diff = max(dot(norm, lightDir), 0.0);
    vec3 diffuse = diff * vec3(1,1,1);

    vec4 diffuse_result = vec4(v_color0/2 +  diffuse/5,1);

    gl_FragColor = mix(diffuse_result, _fog_color, alpha);


	//In this example the color component from the vertex shader is not used
	//gl_FragColor = v_color0;
	//gl_FragColor = texture2D(s_tex,v_texcoord0);
}