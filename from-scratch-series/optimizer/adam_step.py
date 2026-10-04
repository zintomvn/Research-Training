import numpy as np

def adam_step(param, grad, m, v, t, lr=1e-3, beta1=0.9, beta2=0.999, eps=1e-8):
    """
    One Adam optimizer update step.
    Return (param_new, m_new, v_new).
    """
    # Write code here
    param = np.array(param, dtype=np.float64)
    m = np.array(m, dtype=np.float64)
    v = np.array(v, dtype=np.float64)
    grad = np.array(grad, dtype=np.float64)
    
    # step 1: calculate moment 1
    m_new = beta1 * m + (1 - beta1) * grad

    # step 2: calculate moment 2
    v_new = beta2 * v + (1 - beta2) * grad ** 2

    # step 3: bias correction
    m_e_t = m_new / (1 - beta1 ** t)
    v_e_t = v_new / (1 - beta2 ** t)

    # step 4: update
    param_new = param - lr * (m_e_t) / (np.sqrt(v_e_t) + eps) 

    return param_new, m_new, v_new


