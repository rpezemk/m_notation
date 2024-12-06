from jinja2 import Template


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
{% for instrument in instruments %}
{{ instrument }}
{% endfor %}
</CsInstruments>
<CsScore>
{% for event in events -%}
  {{ event }}
{% endfor -%}
</CsScore>
</CsoundSynthesizer>
"""


def get_whole_body(options: list, runtime_data:list, instruments: list, events: list):
    res = Template(synth).render(options=options, runtime_data=runtime_data, instruments=instruments, events=events)
    return res
