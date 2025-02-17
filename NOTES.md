## PWM 
position weight matrices, PWMs用来表示蛋白质-DNA结合特异性

protein binding affinity to DNA/RNA depends on the sequence
通常会允许DNA/RNA序列中某些位置碱基不匹配

[https://pmc.ncbi.nlm.nih.gov/articles/PMC4101922/](https://pmc.ncbi.nlm.nih.gov/articles/PMC4101922/)

## PSSM
position specific scoring matrix, PSSM用来表示蛋白质-DNA结合特异性

PSSM is a normalized version of PWM

## PSSM vs PWM
- PSSM is a normalized version of PWM
- PSSM is a log-odds matrix, which is a measure of the probability of a particular base at a particular position in a sequence
- PWM is a matrix of probabilities of a particular base at a particular position in a sequence
- PSSM is used to calculate the binding affinity of a protein to a DNA/RNA sequence
- PWM is used to calculate the probability of a particular base at a particular position in a sequence

基本结构：
- 矩阵行：序列位置（position 1到N）   
- 矩阵列：4种核苷酸（A/T/C/G）   
- 矩阵值：该位置出现特定碱基的概率权重   

构建步骤：
1. 收集已知结合位点的DNA序列（alignment）
2. 统计每个位置各碱基出现频率
3. 应用伪计数（pseudocount）避免零概率
4. 计算位置概率矩阵：
   PWM[i][b] = (count(b,i) + pseudocount) / (N + 4*pseudocount)
   （i: 位置，b: 碱基，N: 序列总数）
5. 通常转换为log形式方便计算：
   PWM_log[i][b] = log2(PWM[i][b]/background[b])

示例计算：假设有3个结合序列，位置1观测到A出现2次，背景概率0.25，使用伪计数1：
PWM[1][A] = (2+1)/(3+41) = 3/7 ≈ 0.4286
PSSM[1][A] = log2(0.4286/0.25) ≈ 0.78