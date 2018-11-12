function [ratio] = ComputeOverlapRatio(rec1, rec2)
  x0 = rec2(1) - rec1(1);
  y0 = rec2(2) - rec1(2);
  w0 = max(0, x0 + rec2(3));
  h0 = max(0, y0 + rec2(4));
  w1 = min(w0, rec1(3));
  h1 = min(h0, rec1(4));
  ratio = w1*h1/(rec1(3)*rec1(4));
end