from jinja2 import Template

from cs_generator.model.cs_model import GlobalVariable


synth = """
<CsoundSynthesizer>
<CsOptions>
{% for option in options -%}
{{ option }}
{% endfor -%}
</CsOptions>
<CsInstruments>
{% for data in runtime_data -%}
{{ data }}
{% endfor -%}
;  GLOBAL VARIABLES
{% for global_var in global_variables %}
{{ global_var.get_variable_def() }}
{% endfor %}
; EO GLOBAL VARIABLES

;  INSTRUMENTS

{% for instrument in numbered_instruments %}

    ; I_NAME: {{ instrument["i_name"] }} 
    ; INSTR_NO: {{ instrument["i_no"] }} 
    instr {{ instrument["i_no"] }}
{{     instrument["body"] }}
    endin
{% endfor %}

;  EO INSTRUMENTS
</CsInstruments>
<CsScore>
{% for ev_dict in all_events %}
  ; ################# INSTR_NO: {{ ev_dict["i_no"] }} ####################
  {% for single_event in ev_dict["instr_events"] -%} 
    i {{ ev_dict["i_no"] }}  {% for k in single_event.keys() %} {{ single_event[k] }} {% endfor %};
  {% endfor -%}
{% endfor %}
</CsScore>
</CsoundSynthesizer>
"""

def get_whole_body(options: list, runtime_data:list, numbered_instruments: list, all_events: list[list[dict]], global_variables: list[GlobalVariable]):
    res = Template(synth).render(options=options, runtime_data=runtime_data, numbered_instruments=numbered_instruments, all_events=all_events, global_variables=global_variables)
    return res
