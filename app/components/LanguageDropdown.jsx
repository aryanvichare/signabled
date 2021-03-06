import { Fragment, useState } from "react";
import { Listbox, Transition } from "@headlessui/react";
import { CheckIcon, SelectorIcon } from "@heroicons/react/solid";

const languages = [
  {
    name: "English",
    svg: "https://lipis.github.io/flag-icon-css/flags/4x3/us.svg",
    code: "en",
  },
  {
    name: "Arabic",
    svg: "https://lipis.github.io/flag-icon-css/flags/4x3/sa.svg",
    code: "ar",
  },
  {
    name: "Chinese",
    svg: "https://lipis.github.io/flag-icon-css/flags/4x3/cn.svg",
    code: "zh",
  },
  {
    name: "Spanish",
    svg: "https://lipis.github.io/flag-icon-css/flags/4x3/es.svg",
    code: "es",
  },
  {
    name: "Hindi",
    svg: "https://lipis.github.io/flag-icon-css/flags/4x3/in.svg",
    code: "hi",
  },
  {
    name: "French",
    svg: "https://lipis.github.io/flag-icon-css/flags/4x3/fr.svg",
    code: "fr",
  },
];

const LanguageDropdown = ({ selected, setSelected }) => {
  return (
    <div className='w-64 ml-4'>
      <Listbox value={selected} onChange={setSelected}>
        <div className='relative mt-1'>
          <Listbox.Button className='relative w-full py-2 pl-3 pr-10 text-left border bg-white rounded-lg cursor-default focus:outline-none focus-visible:ring-2 focus-visible:ring-opacity-75 focus-visible:ring-white focus-visible:ring-offset-orange-300 focus-visible:ring-offset-2 focus-visible:border-indigo-500 sm:text-sm'>
            <span className='block truncate'>{selected.name}</span>
            <span className='absolute inset-y-0 right-0 flex items-center pr-2 pointer-events-none'>
              <SelectorIcon
                className='w-5 h-5 text-gray-400'
                aria-hidden='true'
              />
            </span>
          </Listbox.Button>
          <Transition
            as={Fragment}
            leave='transition ease-in duration-100'
            leaveFrom='opacity-100'
            leaveTo='opacity-0'>
            <Listbox.Options className='z-20 absolute w-full py-1 mt-1 overflow-auto text-base bg-white rounded-md max-h-60 ring-1 ring-black ring-opacity-5 focus:outline-none sm:text-sm'>
              {languages.map((language, idx) => (
                <Listbox.Option
                  key={idx}
                  className={({ active }) =>
                    `${active ? "text-blue-900 bg-blue-100" : "text-gray-900"}
                          cursor-default select-none relative py-2 pl-10 pr-4`
                  }
                  value={language}>
                  {({ selected, active }) => (
                    <div className='flex items-center'>
                      <span
                        className={`${
                          selected ? "font-medium" : "font-normal"
                        } block truncate`}>
                        {language.name}
                      </span>
                      {selected ? (
                        <span
                          className={`${
                            active ? "text-blue-600" : "text-blue-600"
                          }
                                absolute inset-y-0 left-0 flex items-center pl-3`}>
                          <CheckIcon className='w-5 h-5' aria-hidden='true' />
                        </span>
                      ) : (
                        <img
                          className='absolute inset-y-0 left-0 flex items-center mt-2 ml-2 rounded w-6'
                          src={language.svg}
                          alt={language.name}
                        />
                      )}
                    </div>
                  )}
                </Listbox.Option>
              ))}
            </Listbox.Options>
          </Transition>
        </div>
      </Listbox>
    </div>
  );
};

export default LanguageDropdown;
