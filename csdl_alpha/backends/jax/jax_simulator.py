from csdl_alpha.backends.simulator import SimulatorBase, Recorder
from csdl_alpha.backends.jax.graph_to_jax import create_jax_interface
from csdl_alpha.src.graph.variable import Variable
import numpy as np

class JaxSimulator(SimulatorBase):

    def __init__(
            self, 
            recorder:Recorder,
            ):
        super().__init__(recorder)
        self.recorder:Recorder = recorder
        self.initialize_totals = False

        self.hash = None

        self.fwd_func = None
        self.deriv_func = None

    def run_forward(self, *jax_interface_kwargs):
        self.check_if_optimization()

        if self.fwd_func is None:
            self.fwd_func = create_jax_interface(
                list(self.recorder.design_variables.keys()),
                list(self.recorder.objectives.keys())+list(self.recorder.constraints.keys()),
                self.recorder.active_graph,
                *jax_interface_kwargs
            )

        outputs = self.fwd_func({dv:dv.value for dv in self.recorder.design_variables})
        for output in outputs:
            output.set_value(outputs[output])
        
        return self._process_optimization_values()

    def compute_optimization_derivatives(self, *jax_interface_kwargs):
        self.check_if_optimization()

        if self.deriv_func is None:
            self.recorder.start()
            self.build_objective_constraint_derivatives()
            self.recorder.stop()

            opt_derivs = []
            opt_derivs += [self.objective_gradient] if self.objective_gradient is not None else []
            opt_derivs += [self.constraint_jacobian] if self.constraint_jacobian is not None else []

            self.deriv_func = create_jax_interface(
                list(self.recorder.design_variables.keys()),
                opt_derivs,
                self.recorder.active_graph,
                *jax_interface_kwargs
            )

        outputs = self.deriv_func({dv:dv.value for dv in self.recorder.design_variables})
        
        if self.objective_gradient is None:
            return None, outputs[self.constraint_jacobian]
        elif self.constraint_jacobian is None:
            return outputs[self.objective_gradient], None
        else:
            return outputs[self.objective_gradient], outputs[self.constraint_jacobian]