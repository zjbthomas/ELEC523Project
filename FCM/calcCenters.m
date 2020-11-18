% Equ (20)
function centers = calcCenters(img, U, cNum, m)
    centers = zeros(cNum, 1);    

    for k = 1:cNum
        denSum = 0;
        numSum = 0;
        for r = 1:size(img, 1)
            for c = 1:size(img, 2)
                denSum = denSum + U(r, c, k) ^ m;
                numSum = numSum + U(r, c, k) ^ m * double(img(r, c));
            end
        end
        centers(k) = double(numSum) / double(denSum);
    end
end