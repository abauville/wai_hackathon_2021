import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas as pd
import numpy as np
import seaborn as sns
plt.style.use('seaborn')
mpl.rc('font', size=13)
mpl.rc('axes', labelsize='large')
mpl.rc('xtick', labelsize='large')
mpl.rc('ytick', labelsize='large')

plt.rcParams['figure.figsize'] = [20, 10] # For larger plot



# df_IR = pd.read_stata("CDIR61DT/CDIR61FL.DTA", convert_categoricals=False)
df_IR = pd.read_stata("./Data/ZZIR62FL.DTA", convert_categoricals=False)
# Important variables
# background

edu = 'v106'
violence_justified = 'v744' # a-e
age = 'v012'
age_group = 'v013'
litteracy = 'v155'
media_paper = 'v157'
media_radio = 'v158'
media_tv = 'v159'
sample_weight = 'v005' # must be divided by 1e6
ever_married = 'v020'
# residence = 'v025'
time2water = 'v115'

has_elec = 'v119'
has_radio = 'v120'
has_tv = 'v121'

has_fridge='v122'
has_bicycle = 'v123'
has_moto = 'v124'
has_car = 'v125'
religion = 'v130'
ethnicity = 'v131'
type_of_residence='v102'
de_facto_por='v026'
place_of_residence = 'v134'
edu_attainment = 'v149'
relation2household_head='v150'
sex_household_head = 'v151'
age_household_head = 'v152'

has_phone_landline='v153'

#congo data has no data on these things
#has_phone_mobile='v169a'
#use_internet = 'v171a'
#use_internet_last_month = 'v171b'

#wealth_index = 'v191'
wealth_index_congo='v191'

total_child_born = 'v201'
num_sons_died = 'v206'
num_daughters_died = 'v207'
num_dead_child = 'num_dead_child'
num_living_child = 'v218'
#PA: added new question
no_of_young_child= 'v137'
currently_pregnant= 'v213'

selected_for_dom_violence_interview = 'v044'

husband_edu_level = 'v701'# 's904'
#husband_occupation = 's908a'
#resp_occupation = 's913a'
#in congo:
resp_occupation_congo='v717'
husband_occupation_congo='v705'
# Domestic violence
is_currently_in_union= 'v502'
weight_dom_violence = 'd005'
control_issues = 'd101' #a-j
num_control_issues = 'd102'
emotional_violence = "d103" # a-f
emotional_violence_any = 'emotional_violence_any' #'d104'
physical_violence = 'd105' # a-n detailed acts of violence
physical_violence_less_severe = 'd106'
physical_violence_severe = 'd107'
sexual_violence = 'd108'

violence = 'violence'
# any_violence = 'd105' or 'd106' or 'd107'

violence_to_husband ='d112'
partner_drinks_alcohol='d113'
partner_drinks_alcohol_freq = 'd114'
sought_help = 'd119' # a to xk; y=no one
mother_beaten = 'd121'


edu_w = 'v106' # education level women, value =0-3
edu_m = 'mv106' # education level men,
#Age (v012) is recorded in
#completed years, and is typically reported in 5-year groups (v013).
# age_group_w = "v013"
# Info for men is in the Men's individual recode (MR) dataset



list_col0 = ['caseid', 'v000', sample_weight,
            edu, age, age_group, litteracy,
            media_paper, media_radio, media_tv,
            ever_married,
            has_elec, has_radio, has_tv, has_fridge, has_bicycle, has_car, has_moto,
            has_phone_landline, #has_phone_mobile,
            religion, ethnicity, type_of_residence, de_facto_por,
            place_of_residence, age_household_head,
            relation2household_head,
            wealth_index_congo,
            total_child_born, num_living_child,

            husband_edu_level, husband_occupation_congo, resp_occupation_congo,


            selected_for_dom_violence_interview, weight_dom_violence,
            is_currently_in_union, num_control_issues, #emotional_violence_any,
            physical_violence_less_severe, physical_violence_severe, sexual_violence,
            partner_drinks_alcohol, partner_drinks_alcohol_freq, #sought_help,
            mother_beaten
           ]


# df[violence_justified_sum] = df[[violence_justified + letter for letter in 'abcde']].sum(axis=1)
# df[emotional_violence_sum] = df[[emotional_violence + letter for letter in 'abcdef']].sum(axis=1)



# Prepare clean format for multiple questions

# Violence_justified
# =======
'''
V744A                  Beating justified if wife goes out without tell 6103    1    N    I    1    0   No   No
                               0  No
                               1  Yes
                               8  Don't know
                           (m) 9  Missing
                          (na)    Not applicable
'''
# I assume 0 if v744 in [0, 8, 9, na]; 1 otherwise


# Control issues
# =======
'''
D101A                  Husband/partner jealous if respondent talks wit 8272    1    N    I    1    0   No   No
                               0  No
                               1  Yes
                               8  Don't know
                           (m) 9  Missing
                          (na)    Not applicable
'''
# For cleaning: same as previous

# Physical or sexual violence
# =======
'''
D105A                  Ever been pushed, shook or had something thrown 8291    1    N    I    1    0   No   No
                               0  Never
                               1  Often
                               2  Sometimes
                               3  Yes, but not in the last 12 months
                               4  Yes, but frequency in last 12 months missing
                           (m) 9  Missing
                          (na)    Not applicable
'''
# Let's consider true if hit during the past 12 months only
# So, we clean as 0 if d105a in [0, 2,3,4,9,na]


# Emotional violence
# =======
'''
D103A                  Ever been humiliated by husband/partner         8284    1    N    I    1    0   No   No
                               0  Never
                               1  Often
                               2  Sometimes
                               3  Yes, but not in the last 12 months
                               4  Yes, but frequency in last 12 months missing
                           (m) 9  Missing
                          (na)    Not applicable
'''
# Same as physicial violence for cleaning



cleaning_dict = {
     violence_justified: {'num_questions': 5, 'values_0': [8,9]},
     control_issues:     {'num_questions': 10, 'values_0': [8,9]},
     physical_violence:  {'num_questions': 14, 'values_0': [2,3,4,9]},
     emotional_violence: {'num_questions': 6, 'values_0': [2,3,4,9]},
     }

# Add multiple questions to list_col
list_col = list_col0.copy()
for key in cleaning_dict.keys():
    cleaning_dict[key]['list_col'] = [key + letter for letter in 'abcdefghijklmnopqrstuvwxyz'[:cleaning_dict[key]['num_questions']]]
    list_col += cleaning_dict[key]['list_col']

# Create a subset dataframe that contains only the chosen columns
# and only for women who are married and took the domestic violence interview
df = df_IR[list_col].copy()
df = df[df[is_currently_in_union]==1]
df = df[df[selected_for_dom_violence_interview]==1]

#plot barchart on education level

#fig1.suptitle('Respondent Demographic')
#

for key in cleaning_dict.keys():
    df[key + '_sum'] = 0
    for letter in 'abcdefghijklmnopqrstuvwxyz'[:cleaning_dict[key]['num_questions']]:
        df[key + letter].fillna(0, inplace=True) # There shouldn't be missing na because of preselection of samples, but just in case
        for i in cleaning_dict[key]['values_0']:
            df.loc[df[key +  letter] == i,key + letter] = 0
        df[key + '_sum'] += df[key +  letter]

        # Check that assignment is correct
        assert df[key + letter].max() <= 1
#         print(key + letter + ":", df[key + letter].max())

# Feature engineering
df[num_dead_child] = df[total_child_born] - df[num_living_child]

temp = df[[violence_justified + '_sum', physical_violence + '_sum']].copy()
temp['value'] = 1
temp.loc[temp[physical_violence + '_sum']>=1, physical_violence + '_sum']=1
# temp.loc[temp[violence_justified + '_sum']>=1, violence_justified + '_sum']=1
temp_pivot = temp.pivot_table(columns=[physical_violence + '_sum'],
                              index=[violence_justified + '_sum'],
                              values='value',aggfunc='count')




display(temp_pivot)

plt.figure()
plt.subplot(311)
plt.title('Number of respondents for each class of score (only respondent not experience domestic violence)')
sns.barplot(x=temp_pivot.index, y=temp_pivot.loc[:,0])
plt.subplot(312)
plt.title('% of respondents experiencing domestic violence for each class')
sns.barplot(x=temp_pivot.index, y=temp_pivot.loc[:,1]/temp_pivot.loc[:,0])
plt.subplot(313)
plt.title('Number of respondents for each class of score (only respondent experiencing domestic violence)')
sns.barplot(x=temp_pivot.index, y=temp_pivot.loc[:,1])



key = physical_violence
physical_violence_questions_sum = df[[key + letter for letter in 'abcdefghijklmnopqrstuvwxyz'[:cleaning_dict[key]['num_questions']]]].sum()
num_physical_violence_respondent = (df[physical_violence + '_sum']>0).sum()
dp= physical_violence_questions_sum
dn= num_physical_violence_respondent
dp1= dp[dp!=0]
violences=[
          'pushed',
          'slapped',
          'punched',
          'kicked',
          'burned',
          'threatened \n with \n weapons',
          'forced \n unwanted \n sex',
          'forced \n unwanted \n sexual act',
          'hair pull',
          'forced to \n perform \n sexual act'
          ]
yy= dp1/dn
dp1a= {'col1': dp1/dn, 'col3': violences}
dfp = pd.DataFrame(data=dp1a)
dfpp=dfp.sort_values(by=['col1'], ascending=False)
plt.figure()
ax=sns.barplot(y=dfpp.col1, x=dfpp.col3)
ax.set_title('Most common physical domestic violence in Congo')

list_col = [key + letter for letter in 'abcdefghijklmnopqrstuvwxyz'[:cleaning_dict[key]['num_questions']]]
temp = df[list_col]
co_occurence = (temp.T@temp)#.values
for i in range(co_occurence.shape[0]):
    co_occurence.iloc[i,:] /= co_occurence.iloc[i,i]


plt.figure()
axs=sns.heatmap(co_occurence*100,annot=True)
_ = plt.title("Co-occurence of positive physical or sexual violence acts in the last 12 months")
#axs.set_xticklabels(violences)
#axs.set_yticklabels(violences)



import matplotlib

edu_temp2= df[[edu, physical_violence + '_sum', emotional_violence + '_sum']].copy()
edu_temp2['value']=1
edu_temp2.loc[edu_temp2[physical_violence + '_sum']>=1, physical_violence + '_sum']=1
edu_pivot= edu_temp2.pivot_table(columns=[physical_violence + '_sum'],
                              index=[edu],
                              values='value',aggfunc='count')
edu_pivot['perc']= np.round(100*(edu_pivot.loc[:,1]/(edu_pivot.loc[:,0]+edu_pivot.loc[:,1])),1)

plt.figure()
matplotlib.rcParams.update({'font.size': 14})
education_level=[0,1,2,3]
ed_level=[]
for e in education_level:
    ed_level.append((df[edu] == e).sum())
ed_level2= 100*(ed_level/np.sum(ed_level))
edu_percentage=ed_level2*(edu_pivot['perc'].values)*0.01

labels= ['no education', 'primary', 'secondary', 'higher']
hlss=sns.hls_palette(4, s=.4)
hlss1=sns.hls_palette(4, l=.4)
ax=sns.barplot(y=labels, x=ed_level2, palette=hlss,
            linewidth = 1)
ax=sns.barplot(y=labels, x=edu_percentage, palette=hlss1,
            linewidth = 1)
ax.set_xticklabels([])


matplotlib.rcParams.update({'font.size': 15})
ocu_gr=[0,1,2,3,4,5,6,7,8,9,10,86]
ocu_grups=[]
for o in ocu_gr:
    ocu_grups.append((df[resp_occupation_congo] == o).sum())
ocu_grups2= 100*(ocu_grups/np.sum(ocu_grups))
ocu_grups22= np.round(ocu_grups2,1)
labels=[                          'Not working',
                                  'Professional/ \n technical/ \n managerial',
                                  'Clerical',
                                  'Sales',
                                  'Agricultural \n (self employed)',
                                  'Agricultural \n (employee)',
                                 ' Services',
                                 ' Skilled Manual',
                                  'Unskilled manual',
                               ' Army',
                               'others']
oi= np.where(ocu_grups22>0)
ocu_grups3= ocu_grups22[oi]
oo = {'col1': ocu_grups22, 'col2': labels}
dfo = pd.DataFrame(data=oo)
dfo= dfo.sort_values(by=['col1'], ascending=False)

temp2= df[[resp_occupation_congo, physical_violence + '_sum', emotional_violence + '_sum']].copy()
temp2['value']=1
temp2.loc[temp2[physical_violence + '_sum']>=1, physical_violence + '_sum']=1
opivot= temp2.pivot_table(columns=[physical_violence + '_sum'],
                              index=[resp_occupation_congo],
                              values='value',aggfunc='count')
opivot['perc']= np.round(100*(opivot.loc[:,1]/(opivot.loc[:,0]+opivot.loc[:,1])),1)
opivot['sum']= opivot.loc[:,0]+opivot.loc[:,1]
opercentage=ocu_grups3*(opivot['perc'].values)*0.01


plt.figure()
ax=sns.barplot(y=dfo.col2, x=dfo.col1, palette='hls', linewidth=1)
#ax.pie(ocu_grups, labels= labels, autopct='%1.1f%%')
#ax.set_xticklabels([])


####AGE GROUP
plt.figure()
age_gr=[1,2,3,4,5,6,7]
age_grups=[]
for a in age_gr:
    age_grups.append((df[age_group] == a).sum())
age_grups2= 100*(age_grups/np.sum(age_grups))
age_grups2=np.round(age_grups2)
ax=sns.barplot(y=age_grups2, x=age_gr, palette="pastel",
            linewidth = 1)
age_temp2= df[[age_group, physical_violence + '_sum', emotional_violence + '_sum']].copy()
age_temp2['value']=1
age_temp2.loc[age_temp2[physical_violence + '_sum']>=1, physical_violence + '_sum']=1
age_pivot= age_temp2.pivot_table(columns=[physical_violence + '_sum'],
                              index=[age_group],
                              values='value',aggfunc='count')
age_pivot['perc']= np.round(100*(age_pivot.loc[:,1]/(age_pivot.loc[:,0]+age_pivot.loc[:,1])),1)
percentage=age_grups2*(age_pivot['perc'].values)*0.01

ax=sns.barplot(y=percentage, x=age_gr, palette="deep",
            linewidth = 1)
#ax.set_xticklabels([])


#labels= ['no education', 'primary', 'secondary', 'higher']
#ax=sns.barplot(y=labels, x=ed_level2, palette="tab20c",
#            linewidth = 1)
#ax.set_xticklabels([])

# have they experienced violence?
exp_violence= (df[physical_violence + "_sum"]>0)
false_count= (~exp_violence).sum()
true_count=(exp_violence).sum()
yesnos=[false_count,true_count ]
labels=['no','yes']
fig, ax= plt.subplots()
ax.pie(yesnos, labels=labels, autopct='%1.1f%%',colors = ['#66b3ff','#99ff99'])
ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.





tor=[1,2]
t_or=[]
for t in tor:
    t_or.append((df[type_of_residence] == t).sum())
labels1=['Urban', 'Rural']
place_groups=[]
ltemp2= df[[type_of_residence, physical_violence + '_sum', emotional_violence + '_sum']].copy()
ltemp2['value']=1
ltemp2.loc[ltemp2[physical_violence + '_sum']>=1, physical_violence + '_sum']=1
lpivot= ltemp2.pivot_table(columns=[physical_violence + '_sum'],
                              index=[type_of_residence],
                              values='value',aggfunc='count')
lpivot['perc']= np.round(100*(lpivot.loc[:,1]/(lpivot.loc[:,0]+lpivot.loc[:,1])),1)

#percentage=age_grups2*(age_pivot['perc'].values)*0.01
vals = np.array([[1421, 228], [3699., 720]])

fig1, ax = plt.subplots()
cmap = plt.get_cmap("gnuplot2")
inner_colors = ['#ff6666', '#ffcc99']
outer_colors = ['#ffb3e6','#c2c2f0']

size = 0.3
ax.pie(vals.sum(axis=1), radius=1, colors=outer_colors, labels=labels1,
       wedgeprops=dict(width=size, edgecolor='w'))

ax.pie(vals.flatten(), radius=1-size, colors=inner_colors,
       wedgeprops=dict(width=size, edgecolor='w'))
ax.set(aspect="equal")
plt.show()

fig2, ax = plt.subplots()
por_label=['Capital city', 'small city', 'town', 'country side']
por=[0,1,2,3]
explode=[0,0, 0, 0.2]
p_o_r=[]
for p in por:
    p_o_r.append((df[place_of_residence]== p).sum())

ltemp3= df[[de_facto_por, physical_violence + '_sum', emotional_violence + '_sum']].copy()
ltemp3['value']=1
ltemp3.loc[ltemp3[physical_violence + '_sum']>=1, physical_violence + '_sum']=1
lpivots= ltemp3.pivot_table(columns=[physical_violence + '_sum'],
                              index=[de_facto_por],
                              values='value',aggfunc='count')
lpivots['perc']= np.round(100*(lpivots.loc[:,1]/(lpivots.loc[:,0]+lpivots.loc[:,1])),1)


fig1, ax = plt.subplots()

cmap = plt.get_cmap("tab20c")
outer_colors = cmap(np.arange(4)*4)
inner_colors = cmap([1, 2, 5, 6, 9, 10, 12, 14])

vals = np.array([[625, 76], [160., 34], [636,118], [3699, 720]])


ax.pie(vals.sum(axis=1), radius=1, colors=outer_colors, labels=por_label,
       wedgeprops=dict(width=size, edgecolor='w'))

ax.pie(vals.flatten(), radius=1-size, colors=inner_colors,
       wedgeprops=dict(width=size, edgecolor='w'))
ax.set(aspect="equal")
plt.show()

#ax.pie(p_o_r, labels= por_label,autopct='%1.1f%%', colors=['#ff9999','#66b3ff','#99ff99','#ffcc99'],
#         explode= explode, startangle=90, shadow= True)
#ax.axis('equal')
plt.show()


# wealth index
plt.figure()
wealth_idx=[1,2,3,4,5]


emosh_violence=(df[emotional_violence + "_sum"]>0)
false_counte= (~emosh_violence).sum()
true_counte=(emosh_violence).sum()
#ser.groupby(level=0).sum()
#df = raw_df.groupby(['account number', 'name'])['ext price'].sum().reset_index()

