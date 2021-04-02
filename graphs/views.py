from django.shortcuts import render
from django.views import View
#%%
from plotly.offline import plot
from plotly.graph_objs import Scatter

#%%

# Create your views here.
class Graph(View):
    template_name = 'american_states.html'

    def get_context_data(self, **kwargs):
        context = {}
        x_data = [0,1,2,3]
        y_data = [x**2 for x in x_data]
        plot_div = plot([Scatter(x=x_data, y=y_data,
                        mode='lines', name='test',
                        opacity=0.8, marker_color='green')],
               output_type='div')
        context['graph'] = plot_div

        return render(self.request, template_name, context)