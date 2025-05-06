import os
import owlready2 as owl
import pandas as pd
from pandas.io.formats.style import Styler
from os.path import exists

OUT_DIR='output'
UD_REP='<wbr>'

def main():

    # Load the ontology
    cruise_path = "cruise.owl"
    crs = owl.get_ontology(cruise_path)
    crs.load()

    # Get toplevel, scenario, and concept namespaces
    cns = "http://www.semanticweb.org/ika/vvmethods/cruise"
    sce = crs.get_namespace("http://www.semanticweb.org/ika/vvmethods/cruise/sce#")
    con = crs.get_namespace("http://www.semanticweb.org/ika/vvmethods/cruise/con#")

    # Extract what we are interested in
    base_scenarios = [c for c in crs.classes() if c.namespace == sce and not list(c.subclasses())]
    superclasses = [c for c in crs.classes() if c.namespace == sce and list(c.subclasses())]
    concepts = [c for c in crs.classes() if c.namespace == con and list(c.subclasses())]
    relations = list(crs.object_properties())

    # Manage the base scenarios
    # Create a dataframe from the classes list
    d_bs = pd.DataFrame(base_scenarios, columns=['class'])

    # Get the additional relevant information
    d_bs['Identifier'] = pd.Series([b.get_name(b) for b in base_scenarios])
    d_bs['Name (de)'] = get_labels(base_scenarios, 'de')
    d_bs['Name (en)'] = get_labels(base_scenarios, 'en')
    d_bs['Superclass'] = get_superclasses(base_scenarios)
    d_bs['Concepts'] = get_bs_concepts(base_scenarios)
    d_bs['Image'] = get_images(base_scenarios)

    # Output the base-scenarios
    to_markdown(d_bs, 'base_scenarios',
                exclude=['class'], 
                prettify=['Superclass', 'Concepts'],
                concept=['Concepts'], 
                codify=['Identifier', 'Superclass'],
                image=[('Image', 'Name (en)')])
    to_html(d_bs, 'base_scenarios',
            exclude=['class' ], 
            prettify=['Superclass', 'Concepts'],
            concept=['Concepts'], 
            codify=['Identifier', 'Superclass'],
            image=[('Image', 'Name (en)')])
    to_excel(d_bs, 'base_scenarios', 'base_scenarios', 
             exclude=['class' ],
             concept=['Concepts'], 
             prettify=['Superclass', 'Concepts'])

    # Manage the superclasses
    d_sc = pd.DataFrame(superclasses, columns=['class'])
    d_sc['Identifier'] = pd.Series([sc.get_name(sc) for sc in superclasses])
    d_sc['Name (de)'] = get_labels(superclasses, 'de')
    d_sc['Name (en)'] = get_labels(superclasses, 'en')
    d_sc['Superclass'] = get_superclasses(superclasses)
    d_sc['Concepts'] = get_concept_usage(superclasses)

     # Output the base-scenarios
    to_markdown(d_sc, 'superclasses', 
                exclude=['class' ], 
                prettify=['Superclass', 'Concepts'], 
                concept=['Concepts'], 
                codify=['Identifier', 'Superclass'])
    to_html(d_sc, 'superclasses', 
            exclude=['class' ], 
            prettify=['Superclass', 'Concepts'], 
            concept=['Concepts'], 
            codify=['Identifier', 'Superclass'])
    to_excel(d_sc, 'superclasses', 'superclasses', 
             exclude=['class' ], 
             prettify=['Superclass', 'Concepts'], 
             concept=['Concepts'])
    
    # Manage the superclasses
    d_cn = pd.DataFrame(concepts, columns=['class'])
    d_cn['Identifier'] = pd.Series([c.get_name(c) for c in concepts])
    d_cn['Name (de)'] = get_labels(concepts, 'de')
    d_cn['Name (en)'] = get_labels(concepts, 'en')
    d_cn['Superclass'] = get_superclasses(concepts)

    # Output the base-scenarios
    to_markdown(d_cn, 'concept',
                exclude=['class' ], 
                codify=['Identifier', 'Superclass'])
    to_html(d_cn, 'concepts',
            exclude=['class' ], 
            codify=['Identifier', 'Superclass'])
    to_excel(d_cn, 'concepts', 'concepts', 
             exclude=['class' ])
    
    # Merged output
    to_multisheet_excel({
        'Base-Scenario': {
            'data':d_bs,
            'exclude':['class' ],
            'concept':['Concepts'],
            'prettify':['Superclass', 'Concepts']
        },
        'Superclasses': {
            'data':d_sc,
            'exclude':['class' ],
            'concept':['Concepts'],
            'prettify':['Superclass', 'Concepts']
            },
        'Concepts': {
            'data':d_cn,
            'exclude':['class' ]
            }
        },'cruise')


def get_labels(classes, lang):
    """Gets the labels specified in the list classes in the given lang
    
    Parameters:
        lang: Language to output the labels ('de' or 'en').
    """
    out = []
    for c in classes:
        l = c.label.get_lang(lang)
        if not l:
            out.append('')
        else:
            out.append(l[0])
    return out


def get_superclasses(classes):
    """Gets the superclasses specified in the list classes"""
    out = []
    n_max = 0
    for c in classes:
        parents = c.is_a
        try:
            out.append([p.get_name(p) for p in parents 
                        if isinstance(p, owl.entity.ThingClass)])
            if len(out[-1]) > n_max:
                n_max = len(out[-1])
        except:
            print([p for p in parents])
            print([type(p) for p in parents])
            out.append([])

    if n_max == 1:
        out = [str(o[0]) for o in out]

    return out


def get_concept_usage(classes):
    """Gets the superclasses specified in the list classes"""
    out = []
    for c in classes:
        con_use = []
        parents = c.is_a
        try:
            for p in parents: 
                if isinstance(p, owl.class_construct.Restriction):
                    con_use.append((p.property.get_name(), p.value.get_name(p.value)))
        except:
            print("Exception adding concepts")
            print([p for p in parents])
            print([type(p) for p in parents])
            con_use.append([])
        
        out.append(con_use)
    return out


def prettify_concept_pairs(concepts, pre="", post=""):
    out = []
    for c in concepts:
        if c:
            if c[0] == 'applies_for_ego':
                out.append("For ego: "+pre+c[1]+post)
            elif c[0] == 'applies_for_obj':
                out.append("For obj: "+pre+c[1]+post)
            elif c[0] == 'applies':
                out.append(pre+c[1]+post)
            else:
                raise ValueError("Unknown type of constriant")

    return out


def to_printable(items, pref="- ", sep="<br />"):
    """Generates a string from the list of strings given
    
    Parameters:
        items: list of Strings to be converted
        pref: Prefix placed before each element
        sep: Separator between the elements e.g. '\n' or '<br />'
    """
    return sep.join([pref+i for i in items])


def codify_field(data, pre, post, breakable_underscore=False):
    if isinstance(data, str):
        if breakable_underscore:
            data = data.replace('_', UD_REP + '_')
        return(pre + data + post)
    else:
        out=[]
        for d in data:
            out.append(codify_field(d, pre, post))
        return out


def to_markdown(data, filename, exclude=[], prettify=[], concept=[], codify=[], image=[]):
    """Write the dataframe to an html file.
    
    Parameters:
        data: Dataframe hosting the data to write
        exclude: columns to be dropped from the dataframe for export
        filename: Name of the output file ('.xlsx' will be appended)
        prettify: list of colums whose multiline content is to be displayed as bullets
        concept: list of columns which specifify of which column hosts concepts
        image: list of columns containing relative paths to images
    """
    
    # Work with a copy of the dataframe
    d = data.copy()

    # Format identifiers nicely
    for c in codify:
        d[c] = pd.Series(codify_field(l, '`', '`' ) for l in d[c])

    # Prettify the concepts
    for c in concept:
        if codify:
            d[c] = pd.Series(prettify_concept_pairs(l, pre='`', post='`') for l in d[c])
        else:
            d[c] = pd.Series(prettify_concept_pairs(l, pre='', post='') for l in d[c])
    
    # Prettify the lines specified (expected to contain lists)
    for p in prettify:
        d[p] = pd.Series(to_printable(l, pref="- ", sep="<br />") for l in d[p])

    # Link the images
    for im in image:
        d[im[0]] = pd.Series(to_md_image(pair[0], pair[1]) for pair in zip(d[im[0]], d[im[1]]))
    
    # Drop what we do not want to print
    d = d.drop(columns=exclude)

    # Write the markdown file
    d.to_markdown(os.path.join(OUT_DIR, filename+".md"))
        


def to_html(data, filename, exclude=[], prettify=[], concept=[], codify=[], image=[]):
    """Write the dataframe to an html file.
    
    Parameters:
        data: Dataframe hosting the data to write
        exclude: columns to be dropped from the dataframe for export
        filename: Name of the output file ('.xlsx' will be appended)
        prettify: list of colums whose multiline content is to be displayed as bullets
        concept: list of columns which specifify of which column hosts concepts
        image: list of columns containing relative paths to images
    """
    
    # Work with a copy of the dataframe
    d = data.copy()

    # Format identifiers nicely
    for c in codify:
        d[c] = pd.Series(codify_field(l, '<code>', '</code>', breakable_underscore=True) for l in d[c])

    # Prettify the concepts
    for c in concept:
        if codify:
            d[c] = pd.Series(prettify_concept_pairs(l, pre='<code>', post='</code>') for l in d[c])
        else:
            d[c] = pd.Series(prettify_concept_pairs(l, pre='', post='') for l in d[c])

    # Prettify the lines specified (expected to contain lists)
    for p in prettify:
        d[p] = pd.Series(to_printable(l, pref="- ", sep="<br />") for l in d[p])

    # Link the images
    for im in image:
        d[im[0]] = pd.Series(to_html_image(pair[0], pair[1]) for pair in zip(d[im[0]], d[im[1]]))
    
    # Drop what we do not want to print
    d = d.drop(columns=exclude)

    # Write the html file
    d.style.to_html(os.path.join(OUT_DIR, filename+".html"))
    
    # To generate with CSS ids for each cell. Might be useful to link.
    # s = Styler(d, uuid='bs', cell_ids=True)
    # s.to_html(filename+".html")


def to_excel(data, filename, sheet, exclude=[], prettify=[], concept=[]):
    """Write the dataframe to an Excel file.
    
    Parameters:
        data: Dataframe hosting the data to write
        exclude: columns to be dropped from the dataframe for export
        filename: Name of the output file ('.xlsx' will be appended)
    """
    
    # Work with a copy of the dataframe
    d = data.copy()

    # Prettify the concepts
    for c in concept:
        d[c] = pd.Series(prettify_concept_pairs(l, pre='', post='') for l in d[c])

    # Prettify the lines specified (expected to contain lists)
    for p in prettify:
        d[p] = pd.Series(to_printable(l, pref="", sep="\n") for l in d[p])
    
    # Drop what we do not want to print
    d = d.drop(columns=exclude)

    # Write to Excel an set a word wrap style to all lines such that
    # they are displayed nicely
    with pd.ExcelWriter(os.path.join(OUT_DIR,filename + '.xlsx'), 
                        engine='xlsxwriter') as writer:
        d.to_excel(writer, sheet_name=sheet)
        workbook  = writer.book
        worksheet = writer.sheets[sheet]
        cell_format = workbook.add_format({'text_wrap': True, 'align': 'top'})
        worksheet.set_column('B:Z', 40, cell_format=cell_format)
        worksheet.set_column(0, 0, 6, cell_format=cell_format)


def to_multisheet_excel(data_dict, filename):
    """Write the dataframe to an Excel file.
    
    Parameters:
        data: Dataframe hosting the data to write
        exclude: columns to be dropped from the dataframe for export
        filename: Name of the output file ('.xlsx' will be appended)
    """
    with pd.ExcelWriter(os.path.join(OUT_DIR,filename + '.xlsx'), 
                            engine='xlsxwriter') as writer:
    
        for data_key in data_dict:

            data = data_dict[data_key]

            # Work with a copy of the dataframe
            d = data['data'].copy()

            # Prettify the concepts
            if 'concept' in data:
                for c in data['concept']:
                    d[c] = pd.Series(prettify_concept_pairs(l, pre='', post='') for l in d[c])

            # Prettify the lines specified (expected to contain lists)
            if 'prettify' in data:
                for p in data['prettify']:
                    d[p] = pd.Series(to_printable(l, pref="", sep="\n") for l in d[p])
            
            # Drop what we do not want to print
            if 'exclude' in data:
                d = d.drop(columns=data['exclude'])

            # Write to Excel an set a word wrap style to all lines such that
            # they are displayed nicely
            d.to_excel(writer, sheet_name=data_key)
            workbook  = writer.book
            worksheet = writer.sheets[data_key]
            cell_format = workbook.add_format({'text_wrap': True, 'align': 'top'})
            worksheet.set_column('B:Z', 40, cell_format=cell_format)
            worksheet.set_column(0, 0, 6, cell_format=cell_format)




def get_bs_concepts(base_scenarios):
    """Goes through the base scenarios and identified the concepts
    associated with their superclasses"""
    all_cons = []
    for bs in base_scenarios:
        parents = bs.ancestors()
        cons = []
        for p in parents:
            if isinstance(p, owl.class_construct.Restriction):
                print("Got a base scenario concept. This is unexpected")
                cons.append((p.property.get_name(), p.value.get_name(p.value)))
            elif isinstance(p, owl.entity.ThingClass):
                ps_parents = p.is_a
                con = None
                for pp in ps_parents:
                    if isinstance(pp, owl.class_construct.Restriction):
                        if con:
                            print("Got two concepts for "+p.get_name(p))
                        con =(pp.property.get_name(), pp.value.get_name(pp.value))
                if con:
                    cons.append(con)
                else:
                    print("Got not concept for "+p.get_name(p))

        all_cons.append(cons)

    return all_cons


def find_image(name):
    return exists('img/' + name + '.png')


def get_images(scenarios):
    out = []
    for s in scenarios:
        if find_image(s.get_name(s)):
            out.append('img/' + s.get_name(s) + '.png')
        else:
            out.append('')
    return out


def to_md_image(img, alt_text):
    if img:
        return f'![{alt_text}](../{img})'
    else:
        return ''
    
def to_html_image(img, alt_text):
    # <img src="img_girl.jpg" alt="Girl in a jacket"> 
    if img:
        return f'<img src="../{img}" alt="{alt_text}">'
    else:
        return ''


if __name__ == "__main__":
    main()
